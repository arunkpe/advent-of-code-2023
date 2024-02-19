import os
from collections import defaultdict

txt_file = "cards.txt"
file_path = os.getcwd() + "/input/" + txt_file


class ScratchCard:
    def __init__(self, game_file: str):
        self.games = defaultdict(set)

        with open(game_file) as file:
            for line in file:
                line = line.strip()
                # print(line)
                card_id, card_numbers = self.tokenizer_sorter(line)
                self.games[card_id] = card_numbers

    def tokenizer_sorter(self, line: str):
        line = line + " "
        line_len = len(line)
        # Let's build a function from scratch
        # Because Seena is a syntactic sugar detecting smartass
        # game = line.split(":")[0]
        colon = ":"
        pipe = "|"
        space = " "
        card_id = []
        winning_numbers = []
        your_numbers = []
        number = []
        colon_flg = 0
        pipe_flg = 0
        digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

        for index in range(line_len):
            letter = line[index]

            if colon_flg == 0:
                if letter != colon:
                    card_id.append(letter)
                else:
                    card_id = "".join(card_id)
                    colon_flg = 1
            elif pipe_flg == 0:
                if letter != space and letter != pipe and letter in digits:
                    number.append(letter)
                elif number:
                    number = "".join(number)
                    winning_numbers.append(int(number))
                    number = []
                elif letter == pipe:
                    pipe_flg = 1
            else:
                if letter != space and letter in digits:
                    number.append(letter)
                elif number:
                    number = "".join(number)
                    your_numbers.append(int(number))
                    number = []

        card_numbers = {"winner": winning_numbers, "your_num": your_numbers}

        return card_id, card_numbers

    def card_game_points(self):
        winners = []
        for game, draw in self.games.items():
            curr_game = len([num for num in draw["your_num"] if num in draw["winner"]])
            if curr_game:
                curr_game = curr_game - 1
                winners.append(pow(2, curr_game))

        return sum(winners)


if __name__ == "__main__":
    card_data = ScratchCard(file_path)
    # input_balls = {"red": 12, "green": 13, "blue": 14}
    # sum_games = cube_count.power_minimum_games(input_balls)
    # print(len(card_data.games))
    sum_games = card_data.card_game_points()
    print(sum_games)
