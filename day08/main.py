from pathlib import Path
import numpy as np
import itertools


def load_map(filename):
    return np.array([list(line.strip()) for line in Path(filename).read_text().splitlines()])


def get_antennas(map):
    return {
        freq: [tuple(coord) for coord in np.argwhere(map == freq)]
        for freq in np.unique(map) if freq != "."
    }
    

def antinodes(map):
    antennas = get_antennas(map)
    nodes = set()
    max_x, max_y = map.shape
    
    for coords in antennas.values():
        for (x, y), (a, b) in itertools.combinations(coords, 2):
            dx, dy = x - a, y - b
            nodes.update({(x + dx, y + dy), (a - dx, b - dy)})
    
    return set(filter(lambda coord: 0 <= coord[0] < max_x and 0 <= coord[1] < max_y, nodes))

print("Part 1:", len(antinodes(load_map("input.txt"))))
