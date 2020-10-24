
from typing import Sequence, Tuple
from collections import Counter, defaultdict, deque


def cumsum(arr):
    """lazy cumulative sum"""
    sum_ = 0
    for elem in arr:
        sum_ += elem
        yield sum_


def num2tuple(num: int, ndigits: int) -> Tuple[int]:
    """build a numeric representation where all numbers
    have the num number of digits, zero-padded if neccesary

    Args:
        num (int): a number
        ndigits (int): [description]

    Usage:
        >>> num2tuple(1, ndigits=2)
        >>> (0, 1)

    Returns:
        Tuple[int]: each element is a digit corresponding to original number
    """
    num = str(num).zfill(ndigits)
    num = tuple([int(d) for d in num])
    return num

def radix_sort(nums: Sequence[int]) -> Sequence[int]:
    """perform a radix sort, a non-comparison algorithm with
    linear time complexity that only operates on integers

    Args:
        nums (Sequence[int]): integers to be sorted

    Returns:
        Sequence[int]: sorted integers
    """
    ndigits = len(str(max(nums)))
    digits = list(range(10))
    nums = [num2tuple(num, ndigits) for num in nums]
    for radix_idx in reversed(range(ndigits)):
        digit2nums = defaultdict(deque)
        for num in nums:
            digit2nums[num[radix_idx]].appendleft(num)
        digits_count_cumsum = cumsum(len(digit2nums[d]) for d in digits)
        digits_count_cumsum = list(digits_count_cumsum)
        n_digits_already_in_input = Counter()
        for digit, digit_count_cumsum in zip(digits, digits_count_cumsum):
            for num in digit2nums[digit]:
                idx_new = digit_count_cumsum - n_digits_already_in_input[digit] - 1
                nums[idx_new] = num
                n_digits_already_in_input.update((digit,))
    return [int("".join(map(str, num))) for num in nums]


if __name__ == "__main__":
    # unit tests
    import random
    for _ in range(100):
        dataset = []
        for _ in range(random.randint(100, 10_000)):  # how many elements
            dataset.append(random.randint(0, 100_000))  # value of those elements
        assert radix_sort(dataset) == sorted(dataset)
