from itertools import pairwise

with open("input.txt", "r") as file:
    reports = [list(map(int, line.split())) for line in file]


def is_safe(report):
    return (
        all(0 < b - a <= 3 for a, b in pairwise(report)) 
        or all(-3 <= b - a < 0 for a, b in pairwise(report)))


print("Part 1:", sum(is_safe(report) for report in reports))
print("Part 2:", sum(
    is_safe(report)
    or any(is_safe(report[:i] + report[i + 1 :]) for i in range(0, len(report)))
    for report in reports))
