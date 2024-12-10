from pathlib import Path
import numpy as np

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def load_heightmap(file_path: str) -> np.ndarray:
    lines = Path(file_path).read_text().splitlines()
    return np.array([list(map(int, line)) for line in lines])


def find_trailheads(heightmap: np.ndarray) -> list[tuple[int, int]]:
    return list(map(tuple, np.argwhere(heightmap == 0)))

def explore(heightmap: np.ndarray, trail: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    results = []
    current_position = trail[-1]
    if heightmap[current_position] == 9:
        results.append(trail)
    else:
        current_height = heightmap[current_position]
        for direction in DIRECTIONS:
            next_position = current_position + direction
            if heightmap[next_position] == current_height + 1:
                results.extend(explore(heightmap, trail + [next_position]))
    return results

def find_trails(heightmap: np.ndarray) -> list[list[tuple[int, int]]]:
    trailheads = find_trailheads(heightmap)
    return [explore(heightmap, trailhead) for trailhead in trailheads]


print("Part 1:", find_trails(load_heightmap("input.txt")))
