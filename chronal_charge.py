import numpy as np

SERIAL_NUMBER = 8868
SIZE = 300


def calc_cell_power(row, col):
    x, y = col + 1, row + 1
    rack_id = x + 10
    power = rack_id * y
    power += SERIAL_NUMBER
    power *= rack_id
    power = int(str(power)[-3]) if power > 99 else 0
    power -= 5
    return power


if __name__ == "__main__":
    grid = [calc_cell_power(*divmod(i, SIZE)) for i in range(SIZE * SIZE)]
    grid_helper = np.array(grid).reshape(SIZE, SIZE)

    square_powers = {}

    for i, cell in enumerate(grid):
        row, col = divmod(i, SIZE)
        row_min = row - 1 if row - 1 >= 0 else row
        row_max = row + 2 if row + 2 <= SIZE else row + 1
        col_min = col - 1 if col - 1 >= 0 else col
        col_max = col + 2 if col + 2 <= SIZE else col + 1

        if row - 1 < 0 or col - 1 < 0 or row + 2 > SIZE or col + 2 > SIZE:
            continue

        adjacent_acres = grid_helper[row_min:row_max, col_min:col_max]
        total_power = np.sum(adjacent_acres)
        square_powers[(col, row)] = total_power

    print(max(square_powers.items(), key=lambda item: item[1]))
