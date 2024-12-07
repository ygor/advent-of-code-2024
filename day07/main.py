from pathlib import Path
from typing import List, Tuple, Callable

Operator = Callable[[int, int], int]


def parse_equations(filename: str) -> List[Tuple[int, List[int]]]:
    equations = []
    for line in Path(filename).read_text().splitlines():
        target, numbers = line.split(": ", 1)
        equations.append((int(target), list(map(int, numbers.split()))))
    return equations


def valid(operators: List[Operator], target: int, numbers: List[int]) -> bool:
    if len(numbers) == 1:
        return numbers[0] == target

    a, b, *rest = numbers
    return any(valid(operators, target, [op(a, b)] + rest) for op in operators)


def solve(equations: List[Tuple[int, List[int]]], operators: List[Operator]) -> int:
    return sum(
        result for result, numbers in equations if valid(operators, result, numbers)
    )


operators = [lambda a, b: a + b, lambda a, b: a * b]
concat = lambda a, b: int(f"{a}{b}")

print("Part 1:", solve(parse_equations("input.txt"), operators))
print("Part 2:", solve(parse_equations("input.txt"), operators + [concat]))
