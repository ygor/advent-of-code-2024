from pathlib import Path
import numpy as np
import itertools


def load_map(filename):
    return np.array(
        [list(line.strip()) for line in Path(filename).read_text().splitlines()]
    )


def antennas(map: np.ndarray) -> list[tuple[int, int]]:
    return [
        [tuple(coord) for coord in np.argwhere(map == freq)]
        for freq in np.unique(map)
        if freq != "."
    ]


def antinodes(map):
    return {
        tuple(pos)
        for points in antennas(map)
        for p1, p2 in itertools.combinations(np.array(list(points)), 2)
        for pos in [p1 + (p1 - p2), p2 + (p2 - p1)]
        if all(0 <= pos) and all(pos < map.shape)
    }


print("Part 1:", len(antinodes(load_map("input.txt"))))
