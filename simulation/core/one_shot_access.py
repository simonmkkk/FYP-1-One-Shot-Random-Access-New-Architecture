# ============================================================================
# one_shot_access - One-Shot Random Access simulation engine
# ============================================================================
#
# Monte Carlo simulation for One-Shot Random Access, with three layers:
# 1. simulate_one_shot_access_single_ac - Single AC simulation (core)
# 2. simulate_group_paging_single_sample - Single complete Group Paging (multi-AC)
# 3. simulate_group_paging_multi_samples - Batch parallel simulation (10^7 scale)
# ============================================================================

import os
import time

import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

from simulation.core.utils.progress_manager import SlidingWindowProgress

# Module-level default RNG (used in non-parallel scenarios)
_default_rng = np.random.default_rng()


# ============================================================================
# Core simulation function
# ============================================================================

def simulate_one_shot_access_single_ac(M: int, N: int, rng: np.random.Generator = None):
    """
    Simulate one Access Cycle (AC) of One-Shot Random Access.

    Args:
        M: Number of UEs attempting access.
        N: Number of available RAOs (Preamble pool size).
        rng: numpy Generator (optional, for parallel independence).

    Returns:
        tuple: (success_raos, collision_raos, idle_raos)
    """
    if rng is None:
        rng = _default_rng

    choices = rng.integers(0, N, size=M)
    rao_usage = np.bincount(choices, minlength=N)

    success_raos = np.sum(rao_usage == 1)
    collision_raos = np.sum(rao_usage >= 2)
    idle_raos = np.sum(rao_usage == 0)

    return success_raos, collision_raos, idle_raos


def simulate_group_paging_single_sample(M: int, N: int, I_max: int, rng=None):
    """
    Simulate one complete Group Paging process (multiple ACs).

    Args:
        M: Total UE count.
        N: RAOs per AC.
        I_max: Maximum number of Access Cycles.
        rng: numpy Generator (optional).

    Returns:
        tuple: (access_success_prob, mean_access_delay, collision_prob)
    """
    remaining_devices = M
    success_count = 0
    success_delay_sum = 0
    total_collision_count = 0

    for ac_index in range(1, I_max + 1):
        if remaining_devices == 0:
            break

        success_raos, collision_raos, _ = simulate_one_shot_access_single_ac(
            remaining_devices, N, rng
        )

        success_count += success_raos
        success_delay_sum += success_raos * ac_index
        total_collision_count += collision_raos
        remaining_devices -= success_raos

    access_success_prob = success_count / M if M > 0 else 0.0
    mean_access_delay = success_delay_sum / success_count if success_count > 0 else -1.0
    total_rao_count = I_max * N
    collision_prob = total_collision_count / total_rao_count if total_rao_count > 0 else 0.0

    return access_success_prob, mean_access_delay, collision_prob


# ============================================================================
# Parallel worker
# ============================================================================

def _simulate_batch_worker(M: int, N: int, I_max: int, batch_size: int, seed: int):
    """
    Batch worker: run multiple simulations in a single process.

    Args:
        M: Total UE count.
        N: RAO count.
        I_max: Max AC count.
        batch_size: Number of simulations in this batch.
        seed: Random seed (from SeedSequence, ensures independence).

    Returns:
        np.ndarray: Shape [batch_size, 3] — (P_S, T_a, P_C) per sample.
    """
    rng = np.random.default_rng(seed)
    batch_results = np.empty((batch_size, 3), dtype=np.float64)

    for i in range(batch_size):
        result = simulate_group_paging_single_sample(M, N, I_max, rng)
        batch_results[i, 0] = result[0]
        batch_results[i, 1] = result[1]
        batch_results[i, 2] = result[2]

    return batch_results


# ============================================================================
# Parallel multi-sample simulation
# ============================================================================

def simulate_group_paging_multi_samples(M: int, N: int, I_max: int, num_samples: int,
                                        num_workers: int):
    """
    Parallel multi-sample simulation (batch optimised).

    Uses ProcessPoolExecutor with SlidingWindowProgress for rich progress bars.

    Args:
        M: Total UE count.
        N: RAO count per AC.
        I_max: Max Access Cycle count.
        num_samples: Total simulation samples.
        num_workers: Parallel worker count (-1 = all CPU cores).

    Returns:
        np.ndarray: Shape [num_samples, 3] — (P_S, T_a, P_C) per sample.
    """
    if num_workers == -1:
        num_workers = os.cpu_count() or 1

    # Chunking strategy: 4x CPU cores for load balancing
    num_chunks = num_workers * 4
    base_chunk_size = num_samples // num_chunks
    remainder = num_samples % num_chunks

    start_time = time.time()
    all_results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Generate independent seeds via SeedSequence
        child_seeds = np.random.SeedSequence().spawn(num_chunks)

        # Submit tasks
        futures = []
        for i in range(num_chunks):
            chunk_size = base_chunk_size + (1 if i < remainder else 0)
            if chunk_size == 0:
                continue
            seed = child_seeds[i].generate_state(1)[0]
            futures.append(executor.submit(
                _simulate_batch_worker, M, N, I_max, chunk_size, seed
            ))

        # Collect results with sliding-window progress bars
        with SlidingWindowProgress(total=num_chunks, total_desc=f"N={N}, M={M}") as pm:
            handles = []
            for i in range(num_chunks):
                chunk_size = base_chunk_size + (1 if i < remainder else 0)
                if chunk_size == 0:
                    continue
                handle = pm.add_task(f"Chunk {i+1}", chunk_size)
                handles.append(handle)

            for future in as_completed(futures):
                batch_res = future.result()
                all_results.append(batch_res)
                chunk_idx = len(all_results) - 1
                if chunk_idx < len(handles):
                    pm.complete_task(handles[chunk_idx])

    final_results = np.vstack(all_results)
    elapsed = time.time() - start_time

    print(f"  Done: {num_samples:,} samples in {elapsed:.2f}s ({num_samples/elapsed:,.0f} samples/s)")

    return final_results


__all__ = [
    "simulate_one_shot_access_single_ac",
    "simulate_group_paging_single_sample",
    "simulate_group_paging_multi_samples",
]
