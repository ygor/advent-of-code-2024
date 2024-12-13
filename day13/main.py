from pathlib import Path
import numpy as np
import re


def claw_machines() -> list[list[tuple[int, int]]]:
    regex_button = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
    regex_prize = re.compile(r"Prize: X\=(\d+), Y\=(\d+)")

    return [
        list(
            tuple(map(int, re.match(pattern, line).groups()))
            for pattern, line in zip(
                [regex_button, regex_button, regex_prize], machine.split("\n", 3)
            )
        )
        for machine in Path("input.txt").read_text().split("\n\n")
    ]


def costs(machine: list[tuple[int, int]], conversion=0) -> int:
    A = np.column_stack([np.array(machine[0]), np.array(machine[1])])
    presses = np.linalg.solve(
        A, np.array(machine[2]) + np.array([conversion, conversion])
    )

    return (
        round(presses[0]) * 3 + round(presses[1])
        if np.all(presses > 0)
        and np.all(np.isclose(np.round(presses), presses, atol=1e-6, rtol=1e-13))
        else 0
    )


print("Part 1:", sum(costs(machine) for machine in claw_machines()))
print("Part 2:", sum(costs(machine, 10000000000000) for machine in claw_machines()))
