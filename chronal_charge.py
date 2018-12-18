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

    for width in range(3, 300):
        for i in range(len(grid)):
            row, col = divmod(i, SIZE)

            row_max = row + width
            col_max = col + width

            if row_max > SIZE or col_max > SIZE:
                continue

            square = grid_helper[row:row_max, col:col_max]
            total_power = np.sum(square)
            square_powers[(col + 1, row + 1, width)] = total_power

    print(max(square_powers.items(), key=lambda item: item[1]))
