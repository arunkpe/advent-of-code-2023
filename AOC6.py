import os

txt_file = "engine.txt"
file_path = os.getcwd() + "/input/" + txt_file


class EngineSchematic:
    def __init__(self, schema_file: str):
        self.numbers = []
        self.number_locations = []
        self.symbol_locations = []

        with open(schema_file) as file:
            line_num = 0
            for line in file:
                line = line.strip()
                if line_num == 0:
                    self.line_len = len(line)
                (
                    numbers,
                    number_locations,
                    symbol_locations,
                ) = self.tokenizer_mapper(line, line_num)

                self.numbers.extend(numbers)
                self.number_locations.extend(number_locations)
                self.symbol_locations.extend(symbol_locations)

                line_num += 1

    def tokenizer_mapper(self, line: str, line_num: int):
        symbols = ["*"]
        number_locations = []
        symbol_locations = []
        numbers = []
        num_builder = []
        num_pos_builder = []
        prev_var = ""
        line_len = self.line_len

        for index, var in enumerate(line):
            if var in symbols:
                symbol_locations.append(index + line_num * line_len + 1)

            if var.isdigit():
                num_builder.append(str(var))
                num_pos_builder.append(index + line_num * line_len + 1)
                if index == line_len - 1:
                    numbers.append("".join(num_builder))
                    number_locations.append(tuple(num_pos_builder))
                    num_builder.clear()
                    num_pos_builder.clear()
            elif prev_var.isdigit():
                numbers.append("".join(num_builder))
                number_locations.append(tuple(num_pos_builder))
                num_builder.clear()
                num_pos_builder.clear()
            prev_var = var

        return (
            numbers,
            number_locations,
            symbol_locations,
        )

    def valid_numbers(self):
        possible_numbers = []
        possible_indices = []
        number_pos = [item for sublist in self.number_locations for item in sublist]
        number_loc = self.number_locations
        symbol_pos = self.symbol_locations
        line_len = self.line_len
        star_adj_nums = []

        for pos in symbol_pos:
            left = pos - 1
            right = pos + 1
            top = pos - line_len
            btm = pos + line_len
            top_l = top - 1
            top_r = top + 1
            btm_l = btm - 1
            btm_r = btm + 1

            margins = divmod(pos, line_len)[1]  # divmod(2,7)[1] for a 7 character line
            if margins == 0:
                check_list = [top, btm, left, top_l, btm_l]
            elif margins == 1:
                check_list = [top, btm, right, top_r, btm_r]
            else:
                check_list = [
                    top,
                    btm,
                    right,
                    top_r,
                    btm_r,
                    left,
                    top_l,
                    btm_l,
                ]

            # Idea is to find all pairs of numbers that border a *
            # list comprehension! check list tells you what the list of valid
            # indices are; the number_location has all tuples which have the num_positions
            # search such that any element of that tuple is in the checklist!
            pair = [
                pair
                for pair in self.number_locations
                if any(elem in check_list for elem in pair)
            ]

            # Now only consider if there are exactly 2 pairs bordering a *
            if len(pair) == 2:
                index = [number_loc.index(x) for x in number_loc if x in pair]
                possible_indices.append(index)

            gear_ratios = [
                int(self.numbers[x]) * int(self.numbers[y]) for x, y in possible_indices
            ]

        return sum(gear_ratios)


if __name__ == "__main__":
    engine_counts = EngineSchematic(file_path)
    part_numbers = engine_counts.valid_numbers()
    print(part_numbers)
