with open("input.txt", "r") as file:
    xs, ys = zip(*[map(int, line.split()) for line in file])

print("Part 1:", sum(abs(y - x) for x, y in zip(sorted(xs), sorted(ys))))
print("Part 2:", sum(x * ys.count(x) for x in xs))
