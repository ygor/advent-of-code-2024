from pathlib import Path
import numpy as np

lines = Path("input.txt").read_text().splitlines()
lab: np.ndarray = np.array([list(line) for line in lines])
padded_lab = np.pad(lab, 1, mode="constant", constant_values="0")
rows, cols = lab.shape


def turn(direction: str):
    return {"^": ">", ">": "v", "v": "<", "<": "^"}[direction]


def move(x, y, direction: str):
    return (
        x + {">": 1, "<": -1}.get(direction, 0),
        y + {"v": 1, "^": -1}.get(direction, 0),
    )


direction = "^"
y, x = tuple(np.argwhere(lab == direction)[0])
visited = {(x, y)}

while x in range(cols) and y in range(rows):
    next_x, next_y = move(x, y, direction)

    if padded_lab[next_y + 1, next_x + 1] == "#":
        direction = turn(direction)
        x, y = move(x, y, direction)
    else:
        x, y = next_x, next_y

    visited.add((x, y))

print("Part 1:", len(visited) - 1)
