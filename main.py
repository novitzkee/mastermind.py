from random import randint


class Game:
    def __init__(self, is_difficult: bool, digits_limit: int = 5, trials_limit: int = 12):
        self.__trials_limit: int = trials_limit
        self.__code: str = Generator(digits_limit, is_difficult).generate_code()

    def check_try(self, tried_code: str) -> str:
        verdict: str = ""
        tmp_code: str = self.__code
        indexes: list[int] = [i for i in range(len(tmp_code))]
        zipped_codes: tuple = tuple(zip(indexes, tmp_code, tried_code))

        for i, code_chr, tried_code_chr in zipped_codes:
            if code_chr == tried_code_chr:
                verdict += '|'
                tmp_code = tmp_code[:i] + '!' + tmp_code[i+1:]
            elif tried_code_chr in self.__code:
                verdict += "'"
            else:
                verdict += ' '

        return verdict


class Generator:
    def __init__(self, digits_limit: int, is_difficult: bool):
        self.__digits_limit: int = digits_limit
        self.__is_difficult: int = is_difficult

    def generate_code(self) -> str:
        code: str = ""
        for _ in range(self.__digits_limit):
            rand_num: str = str(randint(0, 9))

            while self.__is_difficult is False and rand_num in code:
                rand_num = str(randint(0, 9))

            code += rand_num

        return code


if __name__ == '__main__':
    pass
