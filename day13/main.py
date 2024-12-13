from pathlib import Path
import math
import re

def claw_machines(input: str) -> list[list[tuple[int, int]]]:
    regex_button = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
    regex_prize = re.compile(r"Prize: X\=(\d+), Y\=(\d+)")

    return [
        list(
            tuple(map(int, re.match(pattern, line).groups()))
            for pattern, line in zip(
                [regex_button, regex_button, regex_prize], machine.split("\n", 3)
            )
        )
        for machine in input.split("\n\n")
    ]


def costs(machine: list[tuple[int, int]]) -> int:
    (a_x, a_y), (b_x, b_y), (p_x, p_y) = machine

    det_A = a_x * b_y - a_y * b_x
    if det_A == 0:
        return 0
    presses_a = (b_y * p_x - b_x * p_y) / det_A
    presses_b = (a_x * p_y - a_y * p_x) / det_A

    if presses_a.is_integer() and presses_b.is_integer() and presses_a > 0 and presses_b > 0:
        return presses_a * 3 + presses_b
    else:
        return 0


print(
    "Part 1:",
    sum(costs(machine) for machine in claw_machines(Path("input.txt").read_text())),
)
