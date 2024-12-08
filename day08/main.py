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


def antenna_pairs(map: np.ndarray) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    return [
        (p1, p2)
        for points in antennas(map)
        for p1, p2 in itertools.combinations(np.array(list(points)), 2)
    ]


def find_antinodes(
    p1: np.ndarray, p2: np.ndarray, n: int, shape: tuple[int, int]
) -> list[tuple[int, int]]:
    positions = [p1 + n * (p1 - p2), p2 - n * (p1 - p2)]
    return [tuple(pos) for pos in positions if all(0 <= pos) and all(pos < shape)]


def antinodes_p1(map: np.ndarray) -> set[tuple[int, int]]:
    return {
        tuple(pos)
        for p1, p2 in antenna_pairs(map)
        for pos in find_antinodes(p1, p2, 1, map.shape)
    }


def antinodes_p2(map: np.ndarray) -> set[tuple[int, int]]:
    result = set()
    for p1, p2 in antenna_pairs(map):
        n = 0
        while positions := find_antinodes(p1, p2, n, map.shape):
            result.update(positions)
            n += 1
    return result


print("Part 1:", len(antinodes_p1(load_map("input.txt"))))
print("Part 2:", len(antinodes_p2(load_map("input.txt"))))
