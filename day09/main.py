from pathlib import Path
from itertools import chain

EMPTY = "."


def load_memory() -> list[tuple[str, int]]:
    return [
        (str(i // 2) if i % 2 == 0 else EMPTY, int(v))
        for i, v in enumerate(Path("input.txt").read_text())
    ]


def decompress(memory: list[tuple[str, int]]) -> list[str]:
    return list(chain.from_iterable([id] * size for id, size in memory if size > 0))


def find_next_empty(memory: list[str], start: int, end: int) -> int:
    return next((i for i in range(start, end + 1) if memory[i] == EMPTY), end)


def optimise_p1(memory: list[tuple[str, int]]) -> list[str]:
    memory = decompress(memory)
    empty = 0
    for i in range(len(memory) - 1, -1, -1):
        if memory[i] != EMPTY and (empty := find_next_empty(memory, empty, i)) < i:
            memory[empty], memory[i] = memory[i], memory[empty]
    return memory


def find_space(memory: list[tuple[str, int]], size: int, max_index: int) -> int:
    index = 0
    while (memory[index][0] != EMPTY or memory[index][1] < size) and index < max_index:
        index += 1
    return index


def move_file(
    memory: list[tuple[str, int]], to_index: int, from_index: int, id: str, size: int
) -> None:
    memory[to_index] = (EMPTY, memory[to_index][1] - size)
    memory[from_index] = (EMPTY, size)
    memory.insert(to_index, (id, size))


def optimise_p2(memory: list[tuple[str, int]]) -> list[str]:
    index = len(memory) - 1
    while index >= 0:
        id, size = memory[index]
        if id != EMPTY and (empty_index := find_space(memory, size, index)) < index:
            move_file(memory, empty_index, index, id, size)
            index += 1
        index -= 1
    return decompress(memory)


def checksum(memory: list[str]) -> int:
    return sum(int(v) * i for i, v in enumerate(memory) if v != EMPTY)


print("Part 1:", checksum(optimise_p1(load_memory())))
print("Part 2:", checksum(optimise_p2(load_memory())))
