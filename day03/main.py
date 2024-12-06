from pathlib import Path
import re


def run(memory):
    mul_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(mul_pattern, memory)
    return sum(int(a) * int(b) for a, b in matches)


memory = Path("input.txt").read_text()
print("Part 1:", run(memory))

do_pattern = r"do\(\)"
dont_pattern = r"don\'t\(\)"

print(
    "Part 2:",
    sum(
        run(re.split(dont_pattern, segment)[0])
        for segment in re.split(do_pattern, memory)
    ),
)
