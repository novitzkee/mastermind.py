from random import randint


class Game:
    def __init__(self, is_difficult: bool, digits_limit: int = 5, trials_limit: int = 12):
        self.__trials_limit: int = trials_limit
        self.__digits_limit: int = digits_limit
        self.__code: str = Generator(self.__digits_limit, is_difficult).generate_code()

    def __check_try(self, tried_code: str) -> bool:
        verdict_in_place: int = 0
        verdict_in_code: int = 0
        tmp_code: str = self.__code
        indexes: list[int] = [i for i in range(len(tmp_code))]
        zipped_codes: tuple = tuple(zip(indexes, tmp_code, tried_code))

        for i, code_chr, tried_code_chr in zipped_codes:
            if code_chr == tried_code_chr:
                verdict_in_place += 1
                tmp_code = tmp_code[:i] + '!' + tmp_code[i+1:]
            elif tried_code_chr in tmp_code:
                verdict_in_code += 1

        if verdict_in_place == self.__digits_limit:
            print("You are the Winner! Good Job!")
            return True
        else:
            print(f"You have {verdict_in_place} digits on the right place{'s' if verdict_in_place > 1 else ''},"
                  f"and {verdict_in_code} digit{'s' if verdict_in_code > 1 else ''} which "
                  f"{'are' if verdict_in_code > 1 else 'is'} in the code but on wrong place")

            return False

    def __validate_input(self, try_to_validate: str) -> bool:
        if len(try_to_validate) != self.__digits_limit:
            return False

        for char in try_to_validate:
            if char.isdigit() is False:
                return False

    def get_try(self) -> bool:
        got_try: str = input("Type Your guess: ")
        while self.__validate_input(got_try) is False:
            got_try = input("Wrong code! Try again: ")

        return self.__check_try(got_try)


class Generator:
    def __init__(self, digits_limit: int, is_difficult: bool):
        self.__digits_limit: int = digits_limit
        self.__is_difficult: int = is_difficult

    def generate_code(self) -> str:
        code: str = ""
        for _ in range(self.__digits_limit):
            rand_num: str = str(randint(0, 9))

            if self.__is_difficult is True:
                while rand_num in code:
                    rand_num = str(randint(0, 9))

            code += rand_num

        return code


if __name__ == '__main__':
    pass
