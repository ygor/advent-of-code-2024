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


def move(area: np.ndarray, x: int, y: int, direction: str) -> tuple[int, int, str]:
    next_x, next_y = next_pos(x, y, direction)

    if (
        next_x not in range(area.shape[1])
        or next_y not in range(area.shape[0])
        or area[next_y, next_x] != OBSTRUCTION
    ):
        return next_x, next_y, direction
    else:
        return x, y, TURNS[direction]


def leave_area(
    area: np.ndarray, x: int, y: int, direction: str
) -> set[tuple[int, int]]:
    visited = set()
    while x in range(area.shape[1]) and y in range(area.shape[0]):
        visited.add((x, y))
        x, y, direction = move(area, x, y, direction)

    return visited


print("Part 1:", len(leave_area(area, start_x, start_y, start_direction)))


def leave_or_loop_area(area: np.ndarray, x: int, y: int, direction: str) -> bool:
    visited = set()
    while x in range(area.shape[1]) and y in range(area.shape[0]):
        state = (x, y, direction)
        if state in visited:
            print(f"Loop detected at {state}")
            return True
        visited.add(state)
        x, y, direction = move(area, x, y, direction)
    return False


def obstruct(area: np.ndarray, x: int, y: int) -> np.ndarray:
    area = area.copy()
    area[y, x] = OBSTRUCTION

    return area


def count_loops(area: np.ndarray, start_x: int, start_Y: int, direction: str) -> int:
    valid_positions = [
        (a, b)
        for b in range(area.shape[0])
        for a in range(area.shape[1])
        if area[b, a] != OBSTRUCTION and (a, b) != (start_x, start_y)
    ]

    def is_loop_position(pos):
        return leave_or_loop_area(
            obstruct(area, pos[0], pos[1]), start_x, start_y, direction
        )

    with ThreadPoolExecutor() as executor:
        return sum(executor.map(is_loop_position, valid_positions))


print("Part 2:", count_loops(area, start_x, start_y, start_direction))
