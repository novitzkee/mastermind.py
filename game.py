from abc import ABC, abstractmethod
from random import randint


class CodeGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        raise NotImplementedError()


class UniqueSymbolsCodeGenerator(CodeGenerator):
    def __init__(self, code_length: int):
        if (code_length > 10):
            raise AssertionError()
        self.__code_length = code_length

    def generate(self) -> str:
        code: set[int] = set()

        while len(code) < self.__code_length:
            code.add(randint(0, 9))

        return ''.join([str(digit) for digit in code])


class RepeatingSymbolsCodeGenerator(CodeGenerator):
    def __init__(self, code_lenght: int):
        self.__code_length = code_lenght

    def generate(self) -> str:
        return ''.join([str(randint(0, 9) for _ in range(self.__code_length))])


class SecretCode:
    def __init__(self, code: str) -> None:
        self.__code = code

    def compare(self, attempt: str) -> tuple[int, int]:
        guessed_digits_count = sum(1 for _ in filter(lambda t: t[0] == t[1], zip(attempt, self.__code)))
        present_digits_count = sum(1 for digit in attempt if digit in self.__code)
        return (guessed_digits_count, present_digits_count - guessed_digits_count)
