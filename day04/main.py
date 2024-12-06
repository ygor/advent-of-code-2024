import numpy as np
from pathlib import Path
from typing import List
import re

lines = Path("input.txt").read_text().splitlines()
matrix: np.ndarray = np.array([list(line) for line in lines])


def count_xmas(lines: List[List[str]]) -> int:
    return sum(
        len(re.findall("XMAS", "".join(line + line[::-1])))
        for line in lines
    )


def get_diagonals(matrix: np.ndarray) -> List[List[str]]:
    rows, cols = matrix.shape
    return [matrix.diagonal(d).tolist() for d in range(-(rows - 1), cols)]


print(
    "Part 1:",
    count_xmas(matrix.tolist())
    + count_xmas(matrix.T.tolist())
    + count_xmas(get_diagonals(matrix))
    + count_xmas(get_diagonals(np.fliplr(matrix))),
)
