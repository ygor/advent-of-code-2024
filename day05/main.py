from pathlib import Path
from functools import partial
from typing import Dict, List
from collections import defaultdict
from functools import reduce
from toolz import complement, compose

sections = Path("input.txt").read_text().split("\n\n")

rules = dict(
    reduce(
        lambda acc, rule: (lambda key, value: acc[key].append(value) or acc)(
            *rule.split("|", 1)
        ),
        sections[0].split("\n"),
        defaultdict(list),
    )
)
updates = [update.split(",") for update in sections[1].split("\n")]


def is_valid(update, rules: Dict[str, List[str]]) -> bool:
    return all(
        update[i] not in rules or all(x not in update[:i] for x in rules[update[i]])
        for i in range(0, len(update))
    )


def to_value(update: List[str]) -> int:
    return int(update[len(update) // 2])


print(
    "Part 1:",
    sum(map(to_value, filter(partial(is_valid, rules=rules), updates))),
)

invalid_updates = filter(complement(partial(is_valid, rules=rules)), updates)


def fix_update(update: List[str]) -> List[str]:
    result = []
    for page in update:
        if page not in rules:
            result.append(page)
        else:
            index = min(
                (result.index(y) for y in rules[page] if y in result),
                default=len(result),
            )
            result.insert(index, page)
    return result


print("Part 2:", sum(map(compose(to_value, fix_update), invalid_updates)))
