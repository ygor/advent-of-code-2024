from pathlib import Path
import numpy as np


def stones(filename: str) -> list[int]:
    return [int(stone) for stone in Path(filename).read_text().split()]


def change(stone: int) -> list[int]:
    match stone:
        case 0:
            return [1]
        case s if len(str(s)) % 2 == 0:
            return [int("".join(part)) for part in np.array_split(list(str(s)), 2)]
        case s:
            return [s * 2024]


def blink(stones: list[int], times: int) -> list[list[int]]:
    for _ in range(times):
        stones = [change(stone) for stone in stones]
        stones = [item for sublist in stones for item in sublist]
    return stones


print("Part 1:", len(blink(stones("input.txt"), 25)))
