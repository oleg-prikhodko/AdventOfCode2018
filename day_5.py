import re
from itertools import chain
from string import ascii_lowercase, ascii_uppercase

UNIT_PAIRS = [
    (f"{lower}{upper}", f"{upper}{lower}")
    for lower, upper in zip(ascii_lowercase, ascii_uppercase)
]
UNIT_PAIR_PATTERN = re.compile("|".join(chain.from_iterable(UNIT_PAIRS)))


def load_polymer(filename="polymer.txt"):
    with open(filename) as input_file:
        polymer_line = input_file.read().strip()
        return polymer_line


def process(polymer):
    while re.search(UNIT_PAIR_PATTERN, polymer) is not None:
        polymer = re.sub(UNIT_PAIR_PATTERN, "", polymer)
    return len(polymer)


def modify(polymer, unit):
    return re.sub(unit, "", polymer, flags=re.I)


if __name__ == "__main__":
    polymer = load_polymer()
    polymer_mods = {unit: modify(polymer, unit) for unit in ascii_lowercase}
    possible_lengths = {
        unit: process(polymer_mod)
        for unit, polymer_mod in polymer_mods.items()
    }
    print(min(possible_lengths.items(), key=lambda item: item[1]))
