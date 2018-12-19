# import re
from itertools import cycle

TRACKS = None
CARTS = None


class CollisionException(RuntimeError):
    def __init__(self, position):
        message = f"Collision occured at {position}"
        super().__init__(message)


def is_cart(cell):
    return cell == "<" or cell == ">" or cell == "^" or cell == "v"


def is_straight_track(cell):
    return cell == "|" or cell == "-" or cell == "S"


def is_main_diag_curve(cell):
    return cell == "/"


def is_anti_diag_curve(cell):
    return cell == "\\"


def is_intersection(cell):
    return cell == "+"


class Cart:
    def __init__(self, direction, position):
        self.direction = direction
        self.position = position
        self.turn_cycle = cycle("lsr")
        self.dead = False

    def __repr__(self):
        return f"Cart('{self.direction}', {self.position})"

    def move(self):
        row, col = self.position
        next_cell_row, next_cell_col = row, col
        if self.direction == ">":
            next_cell_col += 1
        elif self.direction == "<":
            next_cell_col -= 1
        elif self.direction == "^":
            next_cell_row -= 1
        else:
            next_cell_row += 1

        next_cell = TRACKS[next_cell_row][next_cell_col]

        next_pos = (next_cell_row, next_cell_col)
        for cart in CARTS:
            if not cart.dead and cart.position == next_pos:
                # raise CollisionException((next_cell_row, next_cell_col))
                cart.dead = True
                self.dead = True
                return

        if is_straight_track(next_cell):
            self.position = (next_cell_row, next_cell_col)
        elif is_main_diag_curve(next_cell):
            self.position = (next_cell_row, next_cell_col)
            if self.direction == "^":
                self.direction = ">"
            elif self.direction == "<":
                self.direction = "v"
            elif self.direction == ">":
                self.direction = "^"
            else:
                self.direction = "<"
        elif is_anti_diag_curve(next_cell):
            self.position = (next_cell_row, next_cell_col)
            if self.direction == "^":
                self.direction = "<"
            elif self.direction == "<":
                self.direction = "^"
            elif self.direction == ">":
                self.direction = "v"
            else:
                self.direction = ">"
        elif is_intersection(next_cell):
            turn = next(self.turn_cycle)
            self.position = (next_cell_row, next_cell_col)
            if turn == "l":
                if self.direction == ">":
                    self.direction = "^"
                elif self.direction == "<":
                    self.direction = "v"
                elif self.direction == "^":
                    self.direction = "<"
                else:
                    self.direction = ">"
            elif turn == "r":
                if self.direction == ">":
                    self.direction = "v"
                elif self.direction == "<":
                    self.direction = "^"
                elif self.direction == "^":
                    self.direction = ">"
                else:
                    self.direction = "<"


def load_tracks(filename="tracks.txt"):
    global TRACKS
    with open(filename) as input_file:
        # TRACKS = [line.strip() for line in input_file.readlines()]
        TRACKS = input_file.readlines()
        for r, row in enumerate(TRACKS):
            TRACKS[r] = row.replace("\n", "")


def find_carts():
    global TRACKS, CARTS
    tracks = [list(row) for row in TRACKS]
    CARTS = []
    for row, row_str in enumerate(TRACKS):
        for col in range(len(row_str)):
            if is_cart(TRACKS[row][col]):
                CARTS.append(Cart(TRACKS[row][col], (row, col)))
                tracks[row][col] = "S"
    TRACKS = ["".join(row) for row in tracks]
    # from pprint import pprint
    # pprint(TRACKS)
    # return carts


def print_tracks(carts):
    tracks = [list(row) for row in TRACKS]
    for cart in carts:
        tracks[cart.position[0]][cart.position[1]] = cart.direction

    for row in ["".join(row) for row in tracks]:
        print(row)
    print()


def alive_carts_count():
    return sum(1 for cart in CARTS if not cart.dead)


if __name__ == "__main__":
    load_tracks("tracks.txt")
    find_carts()
    # print(carts)

    while alive_carts_count() > 1:
        # print_tracks(CARTS)
        for cart in CARTS:
            if not cart.dead:
                cart.move()

    for cart in CARTS:
        if not cart.dead:
            # cart.move()
            print(cart.position)
