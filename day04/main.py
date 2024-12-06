import numpy as np
from pathlib import Path
from typing import List

lines = Path("input.txt").read_text().splitlines()
matrix: np.ndarray = np.array([list(line) for line in lines])
rows, cols = matrix.shape


def count_xmas(lines: List[List[str]]) -> int:
    return sum("".join(line + line[::-1]).count("XMAS") for line in lines)


def diagonals(matrix: np.ndarray) -> List[List[str]]:
    return [matrix.diagonal(d).tolist() for d in range(-(rows - 1), cols)]


print(
    "Part 1:",
    count_xmas(matrix.tolist())
    + count_xmas(matrix.T.tolist())
    + count_xmas(diagonals(matrix))
    + count_xmas(diagonals(np.fliplr(matrix))),
)


def is_mas(line: List[str]) -> bool:
    return "".join(line) == "MAS" or "".join(line) == "SAM"


padded = np.pad(matrix, pad_width=1, mode="constant", constant_values=0)

print(
    "Part 2:",
    sum(
        is_mas([padded[x - 1, y - 1], padded[x, y], padded[x + 1, y + 1]])
        and is_mas([padded[x - 1, y + 1], padded[x, y], padded[x + 1, y - 1]])
        for x in range(1, rows)
        for y in range(1, cols)
    ),
)
