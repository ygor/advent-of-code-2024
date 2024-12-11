from pathlib import Path
from math import floor, log10


def stones() -> list[int]:
    return [int(stone) for stone in Path("input.txt").read_text().split()]


def change(stone: int, times: int) -> list[int]:
    if times == 0:
        return [stone]
    if stone == 0:
        return change(1, times - 1)

    num_digits = floor(log10(stone)) + 1
    if num_digits % 2 == 0:
        mid = num_digits // 2
        divisor = 10**mid
        return change(stone // divisor, times - 1) + change(stone % divisor, times - 1)

    return change(stone * 2024, times - 1)


def blink(stones: list[int], times: int) -> list[int]:
    return [item for stone in stones for item in change(stone, times)]


print("Part 1:", len(blink(stones(), 25)))
print("Part 2:", len(blink(stones(), 75)))
