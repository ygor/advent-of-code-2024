from pathlib import Path
from collections import defaultdict, Counter


def stones() -> dict[int, int]:
    numbers = map(int, Path("input.txt").read_text().split())
    return dict(Counter(numbers))


def blink(stones: dict[int, int], count: int) -> int:
    for _ in range(count):
        new_stones = defaultdict(int)
        for value, freq in stones.items():
            if value == 0:
                new_stones[1] += freq
            elif len(str(value)) % 2 == 0:
                s = str(value)
                mid = len(s) // 2
                new_stones[int(s[:mid])] += freq
                new_stones[int(s[mid:])] += freq
            else:
                new_stones[value * 2024] += freq
        stones = new_stones
    return sum(stones.values())


print("Part 1:", blink(stones(), 25))
print("Part 2:", blink(stones(), 75))
