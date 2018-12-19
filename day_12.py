import re
from collections import deque
from itertools import repeat


def load_instructions(filename="pots.txt"):
    with open(filename) as input_file:
        intitial_state = (
            re.search(r"initial state:(.+)", input_file.readline())
            .group(1)
            .strip()
        )
        input_file.readline()
        rules = {
            re.search(r"(.+) =>", line)
            .group(1): re.search(r"=> (.{1})", line)
            .group(1)
            for line in input_file.readlines()
        }
        return intitial_state, rules


if __name__ == "__main__":
    init_state, rules = load_instructions()
    # init_state len is 100
    pot_row = deque(init_state)
    pot_row.extendleft(repeat(".", 500))
    pot_row.extend(repeat(".", 500 * 2))
    # print("".join(pot_row))
    # print(pot_row.index("#"))
    zero_pot_index = 500
    pot_row = "".join(pot_row)

    for _ in range(50000000000):
        matches = {}
        for pattern in rules.keys():
            pattern_compiled = re.compile(re.escape(pattern))
            start_index = 0
            while len(pot_row[start_index:]) >= 5:
                match = pattern_compiled.search(pot_row, pos=start_index)
                if match is None:
                    break

                matches[match.start() + 2] = pattern
                # matches.append(m)
                start_index += 1

        pot_row = list(pot_row)
        for index, pattern in matches.items():
            pot_row[index] = rules[pattern]
        pot_row = "".join(pot_row)

        # if _ % 10 == 0:
        result = 0
        for pot_index, pot in enumerate(pot_row):
            if pot == "#":
                result += pot_index - zero_pot_index
        print(_, result)
    # print(pot_row)
