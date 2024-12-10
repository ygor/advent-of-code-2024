from pathlib import Path
import numpy as np

DIRECTIONS = [np.array((1, 0)), np.array((-1, 0)), np.array((0, 1)), np.array((0, -1))]


def load_heightmap(file_path: str) -> np.ndarray:
    lines = Path(file_path).read_text().splitlines()
    return np.array([list(map(int, line)) for line in lines])


def trailheads(heightmap: np.ndarray) -> list[np.array]:
    return [np.array(pos) for pos in np.argwhere(heightmap == 0)]


def explore(
    heightmap: np.ndarray, trail: list[np.array]
) -> list[list[np.array]]:
    results = []
    current_position = trail[-1]

    if heightmap[tuple(current_position)] == 9:
        results.append(trail)
    else:
        for direction in DIRECTIONS:
            next_position = current_position + direction
            if (
                0 <= next_position[0] < heightmap.shape[0]
                and 0 <= next_position[1] < heightmap.shape[1]
                and heightmap[tuple(next_position)]
                == heightmap[tuple(current_position)] + 1
            ):
                results.extend(explore(heightmap, trail + [next_position]))
    return results


def find_trails(heightmap: np.ndarray) -> list[list[np.array]]:
    result = 0
    for trailhead in trailheads(heightmap):
        trails = explore(heightmap, [trailhead])
        result += len(trails)
    return result


print("Part 1:", find_trails(load_heightmap("input.txt")))
