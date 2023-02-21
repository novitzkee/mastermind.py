from random import randint


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
