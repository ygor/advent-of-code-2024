from pathlib import Path
import numpy as np

DIRECTIONS = [np.array([1, 0]), np.array([-1, 0]), np.array([0, 1]), np.array([0, -1])]


def garden_plot(file_path: str) -> np.ndarray:
    lines = Path(file_path).read_text().splitlines()
    return np.array([list(plants) for plants in lines])


def regions(garden_plot: np.ndarray) -> dict[str, set[tuple[int, int]]]:
    return {
        plant: set(map(tuple, np.argwhere(garden_plot == plant)))
        for plant in np.unique(garden_plot)
    }


def measures(regions: dict[str, set[tuple[int, int]]]) -> dict[str, tuple[int, int]]:
    return {
        plant: (
            sum(
                len([d for d in DIRECTIONS if tuple(np.array(pos) + d) not in region])
                for pos in region
            ),
            len(region),
        )
        for plant, region in regions.items()
    }


print("Part 1:", measures(regions(garden_plot("input.txt"))))
