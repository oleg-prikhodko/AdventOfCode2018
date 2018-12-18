import difflib
from collections import Counter
from itertools import combinations


def load_strings(filename="input_2.txt"):
    with open(filename) as input_file:
        strings = input_file.readlines()
        return [string.strip() for string in strings]


def calc_chesksum(strings):
    has_2_reps_count = 0
    has_3_reps_count = 0
    for string in strings:
        counter = Counter(string)

        for _, count in counter.items():
            if count == 2:
                has_2_reps_count += 1
                break

        for _, count in counter.items():
            if count == 3:
                has_3_reps_count += 1
                break

    return has_2_reps_count * has_3_reps_count


def compare(strings):
    string_length = len(strings[0])
    for a, b in combinations(strings, 2):
        if len(a) != len(b):
            continue
        matcher = difflib.SequenceMatcher(None, a, b)
        matching_blocks = matcher.get_matching_blocks()[:-1]
        if (
            len(matching_blocks) == 1
            and matching_blocks[0].size == string_length - 1
        ):
            return a[
                matching_blocks[0].a : matching_blocks[0].a
                + matching_blocks[0].size
            ]
        elif (
            len(matching_blocks) == 2
            and matching_blocks[0].size + matching_blocks[1].size
            == string_length - 1
        ):
            return (
                a[
                    matching_blocks[0].a : matching_blocks[0].a
                    + matching_blocks[0].size
                ]
                + a[
                    matching_blocks[1].a : matching_blocks[1].a
                    + matching_blocks[1].size
                ]
            )


if __name__ == "__main__":
    # chesksum = calc_chesksum(load_strings())
    # print(chesksum)
    result = compare(load_strings())
    print(result)
