from collections import defaultdict
from itertools import cycle


def read_ints(filepath="input_1.txt"):
    with open(filepath) as input_file:
        # lines = input_file.readlines()
        ints = [int(line) for line in input_file]
        return ints


def find_first_repetition(ints):
    result_freq = 0
    past_freqs = dict()

    for freq_change in cycle(ints):
        result_freq += freq_change
        if result_freq in past_freqs:
            return result_freq
        else:
            past_freqs[result_freq] = 1


if __name__ == "__main__":
    # print(sum(read_ints()))
    repetition = find_first_repetition(read_ints())
    print(repetition)
