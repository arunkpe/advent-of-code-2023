import os
from collections import defaultdict

txt_file = "gamecube.txt"
file_path = os.getcwd() + "/input/" + txt_file


class Cubecount:
    def __init__(self, game_file: str):
        self.games = defaultdict(set)

        with open(game_file) as file:
            for line in file:
                line = line.strip()
                gameid, max_balls = self.tokenizer_sorter(line)
                self.games[gameid] = max_balls

    def tokenizer_sorter(self, line: str):
        balls = {}
        tokens = line.split(":")
        gameid = tokens[0]  # "Game 1" Return 1
        # Not effecient but works
        draws = tokens[1]
        draws = draws.replace(";", ",").split(",")
        draw_tuple = [tuple(item.strip().split(" "))[::-1] for item in draws]

        draw_dict = {}
        # Iterate through each tuple in the list
        for key, value in draw_tuple:
            # Convert value to integer for comparison
            value_int = int(value)
            # Update dictionary if key not in dictionary or found a larger value
            if key not in draw_dict or value_int > int(draw_dict[key]):
                draw_dict[key] = value

        return gameid, draw_dict

    def matching_games(self, input_balls):
        possible_games = []

        for game, max_balls in self.games.items():
            check_flg = all(
                int(value) <= int(input_balls[key]) for key, value in max_balls.items()
            )
            if check_flg:
                possible_games.append(int(game.split(" ")[1]))

        return sum(possible_games)


if __name__ == "__main__":
    cube_count = Cubecount(file_path)
    input_balls = {"red": 12, "green": 13, "blue": 14}
    sum_games = cube_count.matching_games(input_balls)
    print(sum_games)
