from pathlib import Path
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# Constants
DIRECTIONS = {">": (1, 0), "<": (-1, 0), "v": (0, 1), "^": (0, -1)}
TURNS = {"^": ">", ">": "v", "v": "<", "<": "^"}
OBSTRUCTION = "#"


# Read input and initialize the area
def load_area(file_path: str) -> np.ndarray:
    lines = Path(file_path).read_text().splitlines()
    return np.array([list(line) for line in lines])


def find_start(area: np.ndarray, direction: str) -> tuple[int, int]:
    return tuple(np.argwhere(area == direction)[0])


def next_position(x: int, y: int, direction: str) -> tuple[int, int]:
    dx, dy = DIRECTIONS[direction]
    return x + dx, y + dy


def move(area: np.ndarray, x: int, y: int, direction: str) -> tuple[int, int, str]:
    next_x, next_y = next_position(x, y, direction)
    if (
        0 <= next_x < area.shape[1]
        and 0 <= next_y < area.shape[0]
        and area[next_y, next_x] != OBSTRUCTION
    ):
        return next_x, next_y, direction
    return x, y, TURNS[direction]


def leave_area(
    area: np.ndarray, x: int, y: int, direction: str
) -> set[tuple[int, int]]:
    visited = set()
    while 0 <= x < area.shape[1] and 0 <= y < area.shape[0]:
        visited.add((x, y))
        x, y, direction = move(area, x, y, direction)
    return visited


def leave_or_loop_area(area: np.ndarray, x: int, y: int, direction: str) -> bool:
    """Check if the starting position results in a loop."""
    visited = set()
    while 0 <= x < area.shape[1] and 0 <= y < area.shape[0]:
        state = (x, y, direction)
        if state in visited:
            return True
        visited.add(state)
        x, y, direction = move(area, x, y, direction)
    return False


def obstruct(area: np.ndarray, x: int, y: int) -> np.ndarray:
    new_area = area.copy()
    new_area[y, x] = OBSTRUCTION
    return new_area


def count_loops(area: np.ndarray, start_x: int, start_y: int, direction: str) -> int:
    valid_positions = [
        (x, y)
        for y in range(area.shape[0])
        for x in range(area.shape[1])
        if area[y, x] != OBSTRUCTION and (x, y) != (start_x, start_y)
    ]

    def is_loop_position(pos):
        return leave_or_loop_area(
            obstruct(area, pos[0], pos[1]), start_x, start_y, direction
        )

    with ThreadPoolExecutor() as executor:
        return sum(executor.map(is_loop_position, valid_positions))


area = load_area("input.txt")
start_direction = "^"
start_y, start_x = find_start(area, start_direction)

print("Part 1:", len(leave_area(area, start_x, start_y, start_direction)))
print("Part 2:", count_loops(area, start_x, start_y, start_direction))
