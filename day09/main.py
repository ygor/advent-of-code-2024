from pathlib import Path
import itertools


def load_memory() -> list[str]:
    return list(
        itertools.chain.from_iterable(
            [index // 2] * int(value) if index % 2 == 0 else ["."] * int(value)
            for index, value in enumerate(Path("input.txt").read_text())
        )
    )


def optimise(memory: list[str]) -> list[str]:
    empty = 0
    for i in range(len(memory) - 1, -1, -1):
        if memory[i] != ".":
            while memory[empty] != "." and empty < i:
                empty += 1
            if empty < i:
                memory[empty], memory[i] = memory[i], "."
    return memory


def checksum(memory: list[str]) -> int:
    return sum(
        int(value) * index
        for value, index in zip(memory, itertools.count())
        if value != "."
    )


print("Part 1:", checksum(optimise(load_memory())))
