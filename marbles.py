from collections import deque
from itertools import cycle


class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.score = 0


class Game:
    def __init__(self, num_players, num_marbles):
        self.circle = deque([0])
        self.players = [Player(i) for i in range(1, num_players + 1)]
        self.num_marbles = num_marbles

    def place_marble(self, player, marble):
        if marble % 23 == 0:
            self.circle.rotate(7)
            player.score += marble + self.circle.pop()
            self.circle.rotate(-1)
        else:
            self.circle.rotate(-1)
            self.circle.append(marble)

    def run(self):
        players_cycle = cycle(self.players)

        for marble in range(1, self.num_marbles + 1):
            current_player = next(players_cycle)
            self.place_marble(current_player, marble)

        return max(self.players, key=lambda player: player.score)


if __name__ == "__main__":
    game = Game(491, 71058 * 100)
    top_player = game.run()
    print(top_player.id, top_player.score)
