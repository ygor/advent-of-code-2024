from pathlib import Path
import itertools


def load_memory():
    return list(
        itertools.chain.from_iterable(
            [index // 2] * int(value) if index % 2 == 0 else ["."] * int(value)
            for index, value in enumerate(Path("input.txt").read_text())
        )
    )


print("Part 1:", load_memory())
