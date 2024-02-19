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
                    if letter in digits:
                        card_id.append(letter)
                else:
                    card_id = int("".join(card_id))
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
            winner = [num for num in draw["your_num"] if num in draw["winner"]]
            winners.append(len(winner))
            self.games[game].update({"wincount": len(winner)})
        return 0

    def card_game_sequences(self):
        repeat_sequence = []
        orig_games = []
        for game, draw in self.games.items():
            # print(draw)
            game_num = game
            seq = list(range(game_num + 1, game_num + 1 + draw["wincount"]))
            repeat_sequence.extend(seq)
            orig_games.append(game)
            self.games[game].update({"repeat_sequence": seq})

        add_seq = []
        add_seq.extend(orig_games)
        add_seq.extend(repeat_sequence)
        for num in repeat_sequence:
            seq = self.recursive_search(num)
            add_seq.extend(seq)
            # print(num, len(add_seq))

        r = len(add_seq)
        return r

    def recursive_search(self, num):
        add_seq = []
        if num == len(self.games):
            return []
        else:
            draw = self.games[num]
            sequence = draw["repeat_sequence"]
            add_seq.extend((sequence))
            for n in sequence:
                add_seq.extend(self.recursive_search(n))

        return add_seq


if __name__ == "__main__":
    card_data = ScratchCard(file_path)
    # sum_games = cube_count.power_minimum_games(input_balls)
    # print(len(card_data.games))
    sum_games = card_data.card_game_points()
    rep = card_data.card_game_sequences()
    print(rep)
