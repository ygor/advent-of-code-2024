from pathlib import Path
import numpy as np

DIRECTIONS = [np.array([1, 0]), np.array([-1, 0]), np.array([0, 1]), np.array([0, -1])]


def garden_plot(file_path: str) -> np.ndarray:
    lines = Path(file_path).read_text().splitlines()
    return np.array([list(plants) for plants in lines])


def plants(garden_plot: np.ndarray) -> dict[str, set[tuple[int, int]]]:
    return {
        plant: set(map(tuple, np.argwhere(garden_plot == plant)))
        for plant in np.unique(garden_plot)
    }


def regions(
    plants: dict[str, set[tuple[int, int]]],
) -> dict[str, list[set[tuple[int, int]]]]:
    regions = {}
    for plant, positions in plants.items():
        regions[plant] = []
        unvisited = positions.copy()

        while unvisited:
            region = set()
            stack = [unvisited.pop()]

            while stack:
                pos = stack.pop()
                region.add(pos)
                neighbors = {tuple(np.array(pos) + d) for d in DIRECTIONS} & unvisited
                unvisited -= neighbors
                stack.extend(neighbors)

            regions[plant].append(region)
    return regions


def measures(
    regions: dict[str, list[set[tuple[int, int]]]],
) -> dict[str, list[tuple[int, int]]]:
    return {
        plant: [
            (
                sum(
                    sum(tuple(np.array(pos) + d) not in region for d in DIRECTIONS)
                    for pos in region
                ),
                len(region),
            )
            for region in regions[plant]
        ]
        for plant in regions
    }


def price(measures: dict[str, list[tuple[int, int]]]) -> int:
    return sum(
        (
            sum(region[0] * region[1] for region in measures[plant])
            for plant in measures.keys()
        )
    )


print("Part 1:", price(measures(regions(plants(garden_plot("input.txt"))))))
