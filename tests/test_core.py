import pytest

from collatzviz.core import collatz_next, collatz_sequence, stopping_time, total_stopping_time


def test_collatz_next_small():
    assert collatz_next(1) == 4
    assert collatz_next(2) == 1
    assert collatz_next(3) == 10


def test_sequence_basic():
    seq = collatz_sequence(6)
    # 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
    assert seq[0] == 6
    assert seq[-1] == 1
    assert 10 in seq and 16 in seq


def test_stopping_times():
    assert stopping_time(1) == 0
    assert total_stopping_time(1) == 0
    # Known values
    assert total_stopping_time(6) == len(collatz_sequence(6)) - 1


def test_invalid():
    with pytest.raises(ValueError):
        collatz_next(0)
    with pytest.raises(ValueError):
        collatz_sequence(0)
