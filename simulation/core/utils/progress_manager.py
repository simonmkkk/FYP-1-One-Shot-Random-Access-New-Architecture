# ============================================================================
# SlidingWindowProgress - Rich-based sliding window progress display
# ============================================================================
#
# Layout:
#   Total ██████████░░░░░░░░░░ 3/10 [0:00:15 < 0:00:35]
#     Task 1  ████████████░░░░░░░░ 6000/10000 [1.2k/s]
#     Task 2  ████░░░░░░░░░░░░░░░░ 2000/10000 [800/s]
#     Task 3  ░░░░░░░░░░░░░░░░░░░░    0/10000
#     Task 4  ░░░░░░░░░░░░░░░░░░░░    0/10000
#     Task 5  ░░░░░░░░░░░░░░░░░░░░    0/10000
#
# Sliding rule:
#   - Completed tasks stay visible (at 100%) so the final state remains on
#     screen after everything finishes.
#   - A completed bar is only evicted when there is a pending task that needs
#     the slot (oldest-completed-first eviction policy).
# ============================================================================

import os
import sys
import threading
import time
from collections import deque
from typing import Optional

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


class SlidingWindowProgress:
    """
    Sliding window terminal progress display built on rich.

    One persistent total bar sits at the top.  Below it, a window of up to
    ``WINDOW_SIZE`` sub-task bars is shown.

    Completed tasks stay visible at 100 % so the final state is preserved on
    screen.  A completed bar is evicted (hidden) only when a new pending task
    needs the slot — oldest-completed-first.

    Thread-safe: ``update`` and ``complete_task`` may be called from any
    thread simultaneously.
    """

    WINDOW_SIZE: int = 5
    PLAIN_REPORT_STEP_PERCENT: int = 5

    def __init__(self, total: int, total_desc: str = "Total") -> None:
        self._lock = threading.Lock()
        self._total = total
        self._total_desc = total_desc
        self._total_task_id: Optional[TaskID] = None
        self._interactive = self._supports_live_rendering()
        self._progress: Optional[Progress] = None
        self._completed_total = 0
        self._plain_next_report = self.PLAIN_REPORT_STEP_PERCENT
        self._plain_started_at = 0.0

        if self._interactive:
            self._progress = Progress(
                SpinnerColumn(),
                TextColumn("[bold]{task.description:<48}"),
                BarColumn(bar_width=36),
                MofNCompleteColumn(),
                TimeElapsedColumn(),
                TimeRemainingColumn(),
                refresh_per_second=10,
                expand=False,
            )

        # Handles currently visible in the window (list of dicts)
        self._window_slots: list = []
        # Tasks registered but waiting for a window slot
        self._pending_queue: deque = deque()

    # ── context-manager support ───────────────────────────────────────────────

    def start(self) -> "SlidingWindowProgress":
        if self._interactive and self._progress is not None:
            self._progress.start()
            self._total_task_id = self._progress.add_task(
                f"[bold green]{self._total_desc}",
                total=self._total,
            )
        else:
            self._plain_started_at = time.time()
            print(f"{self._total_desc} (plain progress mode)")
        return self

    def stop(self) -> None:
        if self._interactive and self._progress is not None:
            self._progress.stop()

    def __enter__(self) -> "SlidingWindowProgress":
        return self.start()

    def __exit__(self, *_) -> None:
        self.stop()

    # ── public API ────────────────────────────────────────────────────────────

    def add_task(self, description: str, total: int) -> dict:
        """
        Register a sub-task.

        If there is a free window slot the task becomes visible immediately;
        otherwise it is queued and will appear once a running task finishes.

        Returns a *handle* dict that must be passed to ``update`` and
        ``complete_task``.
        """
        handle: dict = {
            "desc": description,
            "total": total,
            "rich_id": None,
            "done": False,
            "completed": 0,
        }
        if not self._interactive:
            return handle
        with self._lock:
            if len(self._window_slots) < self.WINDOW_SIZE:
                self._show_in_window(handle)
            else:
                self._pending_queue.append(handle)
        return handle

    def update(
        self,
        handle: dict,
        *,
        completed: Optional[int] = None,
        advance: Optional[int] = None,
    ) -> None:
        """
        Update a sub-task's progress bar.

        Pass either ``completed`` (absolute value) or ``advance`` (delta).
        No-ops if the handle has no rich task id yet (task still queued).
        """
        with self._lock:
            current = int(handle.get("completed", 0))
            total = int(handle.get("total", 0))

            if completed is not None:
                # Absolute updates must never move backward; keep monotonic.
                new_completed = max(current, int(completed))
            elif advance is not None:
                # Ignore non-positive deltas to avoid regressions/noise.
                delta = int(advance)
                if delta <= 0:
                    return
                new_completed = current + delta
            else:
                return

            # Clamp to valid bounds.
            if total >= 0:
                new_completed = min(new_completed, total)
            new_completed = max(0, new_completed)
            handle["completed"] = new_completed

            if not self._interactive:
                return
            rid: Optional[TaskID] = handle.get("rich_id")
            if rid is None or self._progress is None:
                return
            self._progress.update(rid, completed=new_completed)

    def complete_task(self, handle: dict) -> None:
        """
        Mark a sub-task as finished.

        Fills the bar to 100 % and keeps it visible so the final state is
        preserved on screen.  Advances the total bar.

        Promotion rule: when a *visible* task completes, the oldest completed
        bar in the window is evicted and the next pending task is promoted.
        If that promoted task is already done, the cycle repeats so the
        window always shows active (in-progress) tasks when possible.
        """
        if not self._interactive:
            with self._lock:
                handle["done"] = True
                handle["completed"] = handle["total"]
                self._completed_total += 1
                self._maybe_report_plain_progress(handle["desc"])
            return

        with self._lock:
            handle["done"] = True
            rid: Optional[TaskID] = handle.get("rich_id")

            if rid is not None:
                # Visible task finished — fill to 100 %, stay on screen.
                self._progress.update(rid, completed=handle["total"])

            # Always advance the overall total bar.
            self._progress.advance(self._total_task_id)

            # Promote pending tasks into the window.  Loop so that
            # already-done pending tasks are cycled through immediately
            # instead of occupying a window slot with a stale 100 % bar.
            if rid is not None:
                self._promote_pending_tasks()

    # ── internal helpers ──────────────────────────────────────────────────────

    def _promote_pending_tasks(self) -> None:
        """
        Promote pending tasks into the window.  Caller must hold ``_lock``.

        Loop: evict the oldest completed bar → promote the next pending task.
        If the promoted task is already done (it completed while queued),
        fill its bar to 100 % and repeat so the window stays populated
        with *active* tasks whenever possible.
        """
        while self._pending_queue:
            completed_in_window = [h for h in self._window_slots if h["done"]]
            if not completed_in_window:
                break  # no slot to free

            # Evict oldest completed bar
            evict = completed_in_window[0]
            evict_rid: Optional[TaskID] = evict.get("rich_id")
            if evict_rid is not None:
                self._progress.update(evict_rid, visible=False)
            self._window_slots = [h for h in self._window_slots if h is not evict]

            # Promote next pending task
            next_handle = self._pending_queue.popleft()
            self._show_in_window(next_handle)

            if next_handle["done"]:
                # Already finished while queued — fill to 100 % and loop
                self._progress.update(
                    next_handle["rich_id"], completed=next_handle["total"]
                )
                continue  # try to evict this one too and promote another
            else:
                break  # promoted an active task — done

    def _show_in_window(self, handle: dict) -> None:
        """
        Add *handle* to the visible window.  Caller must hold ``_lock``.
        """
        total = int(handle.get("total", 0))
        completed = int(handle.get("completed", 0))
        if total >= 0:
            completed = min(completed, total)
        completed = max(0, completed)
        handle["completed"] = completed

        rich_id: TaskID = self._progress.add_task(
            f"  {handle['desc']}",
            total=handle["total"],
            completed=completed,
            visible=True,
        )
        handle["rich_id"] = rich_id
        self._window_slots.append(handle)

    def _supports_live_rendering(self) -> bool:
        """
        Return True when the current terminal can handle live rich output.
        """
        if os.environ.get("OSRA_PLAIN_PROGRESS", "").lower() in {"1", "true", "yes"}:
            return False
        if not sys.stdout.isatty():
            return False
        if os.environ.get("TERM", "").lower() == "dumb":
            return False
        return True

    def _maybe_report_plain_progress(self, latest_desc: str) -> None:
        """
        Emit occasional progress lines in non-interactive environments.
        """
        if self._total <= 0:
            return

        pct = int((self._completed_total * 100) / self._total)
        should_report = (
            self._completed_total == 1
            or self._completed_total == self._total
            or pct >= self._plain_next_report
        )
        if not should_report:
            return

        elapsed = time.time() - self._plain_started_at
        print(
            f"  Progress: {self._completed_total}/{self._total} "
            f"({pct}%) - latest: {latest_desc} - elapsed: {elapsed:.1f}s"
        )
        while self._plain_next_report <= pct:
            self._plain_next_report += self.PLAIN_REPORT_STEP_PERCENT


__all__ = ["SlidingWindowProgress"]
