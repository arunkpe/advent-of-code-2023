import os
from collections import defaultdict  # You might find this useful


txt_file = "../46threevqs8114.txt"
# txt_file = "test.txt"
file_path = os.getcwd() + "/" + txt_file

number_dict = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

replace_dict = {
    "one": "o1ne",
    "two": "t2wo",
    "three": "t3hree",
    "four": "f4our",
    "five": "f5ive",
    "six": "s6ix",
    "seven": "s7even",
    "eight": "e8ight",
    "nine": "n9ine",
}


class Calibration:
    def __init__(self, words_file: str):
        # Use open() to open the file, and remember to split up words by word length!
        self.calibrations = defaultdict(set)
        number_keys = [key for key in number_dict]
        with open(words_file) as file_obj:
            line_num = 0
            for line in file_obj:
                word = line.strip()
                word_len = len(word)
                first_flg = 0
                last_flg = 0

                if word_len > 0:
                    for number in number_keys:
                        word = word.replace(number, replace_dict[number])

                    word_len = len(word)

                    for pos_lr in range(word_len):
                        if word[pos_lr].isdigit() and first_flg == 0:
                            first_num = word[pos_lr]
                            first_flg = 1
                            break

                    for pos_rl in range(word_len - 1, -1, -1):
                        if word[pos_rl].isdigit() and last_flg == 0:
                            last_num = word[pos_rl]
                            last_flg = 1
                            break

                    line_calibration = int(first_num) * 10 + int(last_num)
                    self.calibrations[line_num].add(line_calibration)
                line_num += 1

    def calculate_line_calibration(self):
        calibrations = list(self.calibrations.values())
        calibrations = [item for calibrations in calibrations for item in calibrations]
        calibration_sum = sum(calibrations)
        return calibration_sum


if __name__ == "__main__":
    print(Calibration(file_path).calculate_line_calibration())
