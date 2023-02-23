

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from parsing import Parser, YesOrNo, parse_int, parse_yes_or_no, sanitized, such_that
from utils import to_lowercase

T = TypeVar("T")


# Classes for handling IO operations

class IO(ABC):
    @abstractmethod
    def input(self, prompt: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def output(self, prompt: str) -> None:
        raise NotImplementedError()


class Console(IO):
    def input(self, prompt: str) -> str:
        return input(prompt)

    def output(self, prompt: str) -> None:
        return print(prompt)


# Classes for handling user input prompts

class Prompt(ABC, Generic[T]):
    @abstractmethod
    def get(self) -> T:
        raise NotImplementedError()


class ReapeatingPrompt(Prompt[T]):
    def __init__(self, io: IO, parser: Parser[str, T], request_prompt: str, error_prompt: str):
        self.__io = io
        self.__parse = parser
        self.__request_prompt = request_prompt
        self.__error_prompt = error_prompt

    def get(self) -> T:
        input = self.__perform_prompt()

        while input == None:
            self.__show_error()
            input = self.__perform_prompt()

        return input

    def __perform_prompt(self) -> Optional[T]:
        input = self.__io.input(self.__request_prompt)
        return self.__parse(input)

    def __show_error(self) -> None:
        self.__io.output(self.__error_prompt)


class YesOrNoPrompt(ReapeatingPrompt[YesOrNo]):
    def __init__(self, io: IO, request_prompt: str, error_prompt: str):
        y_or_n_parser = sanitized(parse_yes_or_no, to_lowercase)
        super().__init__(io, y_or_n_parser, request_prompt, error_prompt)


class BoundedIntPrompt(ReapeatingPrompt[int]):
    def __init__(self, io: IO, valid_range: range, request_prompt: str, error_prompt: str):
        int_in_range_parser = such_that(parse_int, lambda i: i in valid_range)
        super().__init__(io, int_in_range_parser, request_prompt, error_prompt)
