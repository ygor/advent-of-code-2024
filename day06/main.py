from pathlib import Path
import numpy as np
from concurrent.futures import ThreadPoolExecutor

DIRECTIONS = {">": (1, 0), "<": (-1, 0), "v": (0, 1), "^": (0, -1)}
TURNS = {"^": ">", ">": "v", "v": "<", "<": "^"}
OBSTRUCTION = "#"

lines = Path("input.txt").read_text().splitlines()
area: np.ndarray = np.array([list(line) for line in lines])

start_direction = "^"
start_y, start_x = tuple(np.argwhere(area == start_direction)[0])


def next_pos(x: int, y: int, direction: str) -> tuple[int, int]:
    dx, dy = DIRECTIONS[direction]
    return x + dx, y + dy


def walk(area: np.ndarray, x: int, y: int, direction: str) -> tuple[int, int, str]:
    next_x, next_y = next_pos(x, y, direction)

    if (
        not (0 <= next_x < area.shape[1] and 0 <= next_y < area.shape[0])
        or area[next_y, next_x] != OBSTRUCTION
    ):
        return next_x, next_y, direction
    else:
        direction = TURNS[direction]
        return *next_pos(x, y, direction), direction


def leave_area(
    area: np.ndarray, x: int, y: int, direction: str
) -> set[tuple[int, int]]:
    visited = set()
    while x in range(area.shape[1]) and y in range(area.shape[0]):
        visited.add((x, y))
        x, y, direction = walk(area, x, y, direction)

    return visited


print("Part 1:", len(leave_area(area, start_x, start_y, start_direction)))


def leave_or_loop_area(area: np.ndarray, x: int, y: int, direction: str) -> bool:
    visited = set()
    loop = False

    while x in range(area.shape[1]) and y in range(area.shape[0]):
        if (x, y, direction) in visited:
            loop = True
            break
        visited.add((x, y, direction))
        x, y, direction = walk(area, x, y, direction)

    return loop


def obstruct(area: np.ndarray, x: int, y: int) -> np.ndarray:
    area = area.copy()
    area[y, x] = OBSTRUCTION

    return area


def count_loops(area: np.ndarray, x: int, y: int, direction: str) -> int:
    positions = [(z, w) for z in range(area.shape[1]) for w in range(area.shape[0])]
    with ThreadPoolExecutor() as executor:
        results = executor.map(
            lambda pos: leave_or_loop_area(
                obstruct(area, pos[0], pos[1]), x, y, direction
            ),
            positions,
        )

    return sum(results)


print("Part 2:", count_loops(area, start_x, start_y, start_direction))
