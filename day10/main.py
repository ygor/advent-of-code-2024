from pathlib import Path
import numpy as np
from typing import Callable

DIRECTIONS = [np.array((1, 0)), np.array((-1, 0)), np.array((0, 1)), np.array((0, -1))]


def load_heightmap(file_path: str) -> np.ndarray:
    lines = Path(file_path).read_text().splitlines()
    return np.array(
        [list(map(lambda x: -1 if x == "." else int(x), line)) for line in lines]
    )


def trailheads(heightmap: np.ndarray) -> list[np.array]:
    return [np.array(pos) for pos in np.argwhere(heightmap == 0)]


def explore(heightmap: np.ndarray, trail: list[np.array]) -> list[list[np.array]]:
    if heightmap[tuple(trail[-1])] == 9:
        return [trail]

    return [
        new_trail
        for d in DIRECTIONS
        if np.all((next_pos := trail[-1] + d) >= 0)
        and np.all(next_pos < heightmap.shape)
        and heightmap[tuple(next_pos)] == heightmap[tuple(trail[-1])] + 1
        for new_trail in explore(heightmap, trail + [next_pos])
    ]


def process_trails(heightmap: np.ndarray, fn: Callable[[list[np.ndarray]], int]) -> int:
    return sum(fn(explore(heightmap, [th])) for th in trailheads(heightmap))


def score_trails(heightmap: np.ndarray) -> int:
    return process_trails(heightmap, lambda trails: len({tuple(trail[-1]) for trail in trails}))


def rate_trails(heightmap: np.ndarray) -> int:
    return process_trails(heightmap, lambda trails: len(trails))


print("Part 1:", score_trails(load_heightmap("input.txt")))
print("Part 2:", rate_trails(load_heightmap("input.txt")))
