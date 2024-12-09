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


def load_memory_p2() -> list[tuple[str, int]]:
    return list(
        (index // 2, int(value)) if index % 2 == 0 else (".", int(value))
        for index, value in enumerate(Path("input.txt").read_text())
    )

def optimise_p2(memory: list[tuple[str, int]]) -> list[str]:
    empty = 0
    index = len(memory) - 1
    while index >= 0:
        id, size = memory[index]
        if id != ".":
            empty = 0
            while (memory[empty][0] != "." or memory[empty][1] < size) and empty < index:
                empty += 1  
            if empty < index:
                space = memory[empty][1]
                memory[empty] = (".", space - size)
                memory[index] = (".", size)
                memory.insert(empty, (id, size))
                index += 1
        index -= 1
    
    return list(itertools.chain.from_iterable([id] * size for id, size in memory if size > 0))


def checksum(memory: list[str]) -> int:
    return sum(
        int(value) * index
        for value, index in zip(memory, itertools.count())
        if value != "."
    )


print("Part 1:", checksum(optimise(load_memory())))
print("Part 2:", checksum(optimise_p2(load_memory_p2())))
