# ============================================================================
# constants - Default simulation parameters
# ============================================================================

# Default simulation parameters
DEFAULT_M: int = 100           # Initial number of UEs (paper setting)
DEFAULT_N: int = 50            # Number of RAOs (Preamble pool size)
DEFAULT_I_MAX: int = 10        # Max Access Cycle count (paper setting)
DEFAULT_NUM_SAMPLES: int = 100000   # Default simulation samples
DEFAULT_NUM_WORKERS: int = -1       # Parallel workers (-1 = all CPU cores)

# ============================================================================
# Module exports
# ============================================================================

__all__ = [
    "DEFAULT_M",
    "DEFAULT_N",
    "DEFAULT_I_MAX",
    "DEFAULT_NUM_SAMPLES",
    "DEFAULT_NUM_WORKERS",
]
