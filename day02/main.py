from itertools import pairwise

with open("input.txt", "r") as file:
    reports = [[int(x) for x in line.split()] for line in file]
    valid_reports = [
        all(0 < b - a <= 3 for a, b in pairwise(report))
        or all(-3 <= b - a < 0 for a, b in pairwise(report))
        for report in reports
    ]
    print(sum(valid_reports))
