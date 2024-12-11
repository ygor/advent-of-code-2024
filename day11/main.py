from pathlib import Path
import numpy as np
from multiprocessing import Pool


def stones() -> list[int]:
    return [int(stone) for stone in Path("input.txt").read_text().split()]


def change(stone: int) -> list[int]:
    match stone:
        case 0:
            return [1]
        case s if len(str(s)) % 2 == 0:
            s = str(s)
            mid = len(s) // 2
            return [int(s[:mid]), int(s[mid:])]
        case s:
            return [s * 2024]


def blink(stones: list[int], times: int) -> list[int]:
    with Pool() as pool:
        for _ in range(times):
            stones = pool.map(change, stones)
            stones = [item for stone in stones for item in stone]
    return stones

print("Part 1:", len(blink(stones(), 75)))
