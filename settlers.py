import numpy as np

test_field = """\
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""".replace(
    "\n", ""
)
SIZE = 50


def load_field_string(filename="settlers.txt"):
    with open(filename) as input_file:
        return "".join(line.strip() for line in input_file.readlines())


def solve(field):
    field_helper = field.copy().reshape(SIZE, SIZE)
    new_field = field.copy()

    for i, acre in enumerate(field):
        row, col = divmod(i, SIZE)

        row_min = row - 1 if row - 1 >= 0 else row
        row_max = row + 2 if row + 2 <= SIZE else row + 1
        col_min = col - 1 if col - 1 >= 0 else col
        col_max = col + 2 if col + 2 <= SIZE else col + 1

        adjacent_acres = field_helper[row_min:row_max, col_min:col_max]

        if acre == "." and np.count_nonzero(adjacent_acres == "|") >= 3:
            new_field[i] = "|"
        elif acre == "|" and np.count_nonzero(adjacent_acres == "#") >= 3:
            new_field[i] = "#"
        elif acre == "#":
            if not (
                np.count_nonzero(adjacent_acres == "#") >= 2
                and np.count_nonzero(adjacent_acres == "|") >= 1
            ):
                new_field[i] = "."

    return new_field


def print_field(field):
    for row in field:
        print("".join(row))
    print("\n")


if __name__ == "__main__":
    # field_string = test_field
    field_string = load_field_string()
    field = np.array(list(field_string))

    time_limit = 1000000000

    # results start to repeat from 1000 iteration with period 7:
    # 1000 188400
    # 2000 176532
    # 3000 202488
    # 4000 206375
    # 5000 183543
    # 6000 179744
    # 7000 216832
    # 8000 188400
    # ...
    # Hence offset is equal to (1_000_000_000 - 1_000) % 7 == 0
    # So 188400 is the answer

    for tick in range(1, time_limit):
        field = solve(field)
        if tick % 1000 == 0:
            wooden_acres = np.count_nonzero(field == "|")
            lumberyards = np.count_nonzero(field == "#")
            print(tick, wooden_acres * lumberyards)

    # wooden_acres = np.count_nonzero(field == "|")
    # lumberyards = np.count_nonzero(field == "#")
    # print(wooden_acres * lumberyards)
