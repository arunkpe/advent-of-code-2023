import os
from collections import defaultdict  # You might find this useful


txt_file = "46threevqs8114.txt"
file_path = os.getcwd() + "/input/" + txt_file


class Calibration:
    def __init__(self, words_file: str):
        # Use open() to open the file, and remember to split up words by word length!
        self.calibrations = defaultdict(set)
        with open(words_file) as file_obj:
            line_num = 0
            for line in file_obj:
                word = line.strip()
                word_len = len(word)
                first_flg = 0
                last_flg = 0
                if word_len > 0:
                    for pos in range(word_len):
                        if word[pos].isdigit() and first_flg == 0:
                            first_num = word[pos]
                            first_flg = 1
                            break
                    for pos in range(word_len - 1, -1, -1):
                        if word[pos].isdigit() and last_flg == 0:
                            last_num = word[pos]
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
