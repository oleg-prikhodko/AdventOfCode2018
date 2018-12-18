from itertools import count, cycle
from operator import add, sub


class Circle:
    def __init__(self):
        self.arr = []
        self.current_marble = None

    def get_marble_index_from_current(self, offset, clockwise=True):
        if self.current_marble is None:
            return None

        current_marble_index = self.arr.index(self.current_marble)
        operation = add if clockwise else sub
        marble_index = operation(current_marble_index, offset) % len(self.arr)
        return marble_index

    def get_marble(self, marble_index):
        return self.arr[marble_index]

    def insert_marble(self, marble):
        if not self.arr or len(self.arr) == 1:
            self.arr.append(marble)
        else:
            insert_index = self.get_marble_index_from_current(2)
            self.arr.insert(insert_index, marble)

        self.current_marble = marble

    def delete_marble(self, marble_index):
        self.current_marble = self.arr[self.get_marble_index_from_current(1)]
        self.arr.remove(self.get_marble(marble_index))


class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.score = 0


class Game:
    def __init__(self, num_players, stop_value):
        self.circle = Circle()
        self.players = [Player(i) for i in range(1, num_players + 1)]
        self.stop_value = stop_value
        self.current_player = None

    def place_marble(self, player, marble):
        if marble % 23 == 0:
            seventh_marble_index = self.circle.get_marble_index_from_current(
                7, False
            )
            seventh_marble = self.circle.get_marble(seventh_marble_index)
            player.score += marble + seventh_marble
            self.circle.delete_marble(seventh_marble_index)
            return marble + seventh_marble

        else:
            self.circle.insert_marble(marble)

    def run(self):
        players_cycle = cycle(self.players)
        marble_sequence = count()

        while True:
            marble = next(marble_sequence)
            if marble == 0:
                self.circle.insert_marble(marble)
            else:
                self.current_player = next(players_cycle)
                marble_worth = self.place_marble(self.current_player, marble)
                if marble_worth is not None:
                    print(marble_worth)
                if marble_worth == self.stop_value:
                    break

        return max(self.players, key=lambda player: player.score)


if __name__ == "__main__":
    game = Game(13, 7999)
    top_player = game.run()
    print(top_player.id, top_player.score)
