from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Iterable, List, Tuple


def collatz_next(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be a positive integer")
    return 3 * n + 1 if n % 2 else n // 2


def collatz_sequence(start: int, limit: int | None = None) -> List[int]:
    """Generate the Collatz sequence from start until reaching 1 or limit length.
    Includes the starting value.
    """
    if start <= 0:
        raise ValueError("start must be positive")
    seq = [start]
    while seq[-1] != 1:
        nxt = collatz_next(seq[-1])
        seq.append(nxt)
        if limit is not None and len(seq) >= limit:
            break
    return seq


def stopping_time(n: int) -> int:
    """Number of steps to first reach a value < n (conventional ‘stopping time’)."""
    if n <= 1:
        return 0
    steps = 0
    x = n
    while x >= n:
        x = collatz_next(x)
        steps += 1
    return steps


def total_stopping_time(n: int) -> int:
    """Number of steps to reach 1 (a.k.a. total stopping time)."""
    if n <= 1:
        return 0
    steps = 0
    x = n
    while x != 1:
        x = collatz_next(x)
        steps += 1
    return steps


@lru_cache(maxsize=None)
def _steps_and_peak_to_one(n: int) -> tuple[int, int]:
    """Memoized helper: returns (steps to 1, peak encountered from n to 1)."""
    if n <= 1:
        return (0, 1)
    m = collatz_next(n)
    s, p = _steps_and_peak_to_one(m)
    return (s + 1, max(n, p))


@dataclass
class RangeStats:
    start: int
    end: int
    stopping_times: Dict[int, int]
    total_stopping_times: Dict[int, int]
    peaks: Dict[int, int]


def collatz_stats_range(start: int, end: int) -> RangeStats:
    if start <= 0 or end <= 0:
        raise ValueError("start and end must be positive")
    if end < start:
        start, end = end, start
    st: Dict[int, int] = {}
    tst: Dict[int, int] = {}
    peaks: Dict[int, int] = {}
    for n in range(start, end + 1):
        if n == 1:
            st[n] = 0
            tst[n] = 0
            peaks[n] = 1
            continue

        # stopping time until first value < n
        x = n
        steps_to_lt = 0
        while x >= n:
            x = collatz_next(x)
            steps_to_lt += 1
        st[n] = steps_to_lt

        # total stopping time and peak via memoized helper
        total_steps, peak = _steps_and_peak_to_one(n)
        tst[n] = total_steps
        peaks[n] = peak
    return RangeStats(start, end, st, tst, peaks)
