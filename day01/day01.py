with open('input.txt', 'r') as file:
    part1 = sum(
        abs(y - x)
        for x, y in zip(
            *map(lambda xs: sorted(map(int, xs)), zip(*[line.split() for line in file]))
        )
    )
    print(part1)