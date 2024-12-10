from pathlib import Path
import numpy as np

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


def find_trails(heightmap: np.ndarray) -> list[list[np.array]]:
    return sum(
        len({tuple(trail[-1]) for trail in explore(heightmap, [th])})
        for th in trailheads(heightmap)
    )


print("Part 1:", find_trails(load_heightmap("input.txt")))
