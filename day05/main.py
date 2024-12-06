from pathlib import Path
from functools import partial
from typing import Dict, List
from collections import defaultdict
from functools import reduce

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
updates = [update.split(",") for update in sections[1].split("\n") if update.strip()]


def is_valid(update, rules: Dict[str, List[str]]) -> bool:
    return all(
        [
            update[i] not in rules or all(x not in update[:i] for x in rules[update[i]])
            for i in range(0, len(update))
        ]
    )


print(
    "Part 1:",
    sum(
        map(
            lambda update: int(update[len(update) // 2]),
            filter(partial(is_valid, rules=rules), updates),
        )
    ),
)
