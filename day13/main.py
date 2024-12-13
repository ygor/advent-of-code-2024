from pathlib import Path
import numpy as np
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
    A = np.column_stack([np.array(machine[0]), np.array(machine[1])])
    presses = np.linalg.solve(A, np.array(machine[2]))

    return (
        round(presses[0]) * 3 + round(presses[1])
        if np.all(presses > 0) and np.all(np.isclose(np.round(presses), presses))
        else 0
    )


print(
    "Part 1:",
    sum(costs(machine) for machine in claw_machines(Path("input.txt").read_text())),
)
