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
        symbols = [
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "+",
            "!",
            "~",
            "(",
            ")",
            "-",
            "/",
            ">",
            "<",
            "?",
            "|",
            "\\",
            "{",
            "}",
            "[",
            "]",
            "=",
            "-",
            "_",
            "`",
            ";",
            ":",
            "'",
        ]
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
            # A bit ugly but I compare if var is digit once
            # Alt - keep prev_index
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

        for pos in number_pos:
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

            check = any((True for x in check_list if x in symbol_pos))

            if check:
                # list comprehension; find index of number position which is bounded by tuple
                index = [number_loc.index(x) for x in number_loc if pos in x][0]
                possible_indices.append(index)

        possible_indices = list(set(possible_indices))
        possible_numbers = [int(self.numbers[index]) for index in possible_indices]

        final_nums = list(possible_numbers)

        return sum(final_nums)


if __name__ == "__main__":
    engine_counts = EngineSchematic(file_path)
    part_numbers = engine_counts.valid_numbers()
    print(part_numbers)
