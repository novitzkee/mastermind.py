

from abc import ABC, abstractmethod
from typing import Generic, Literal, NotRequired, Optional, TypeVar, TypedDict
from parsing import Parser, YesOrNo, YES_OR_NO_PARSER, MULTIFORMAT_INT_PARSER, all_satisfy, has_length, is_contained_by, such_that, parse_string

T = TypeVar("T")


# Wrapper for IO operations


class IO(ABC):
    @abstractmethod
    def input(self, prompt: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def output(self, message: str) -> None:
        raise NotImplementedError()


class Console(IO):
    def input(self, prompt: str) -> str:
        return input(prompt)

    def output(self, message: str) -> None:
        return print(message)


# Classes for handling user input prompts


PromptMessageNames = Literal["ask", "error", "success"]


class PromptMessages(TypedDict):
    ask: str
    error: str
    success: NotRequired[str]


class Prompt(ABC, Generic[T]):
    @abstractmethod
    def get(self) -> T:
        raise NotImplementedError()


class ReapeatingPrompt(Prompt[T]):
    def __init__(self, io: IO, parser: Parser[str, T], prompt_messages: PromptMessages):
        self.__io = io
        self.__parse = parser
        self.__messages = prompt_messages

    def get(self) -> T:
        input = self.__perform_prompt()

        while input == None:
            self.__show_error()
            input = self.__perform_prompt()

        self.__show_success()
        return input

    def __perform_prompt(self) -> Optional[T]:
        input = self.__io.input(self.__messages["ask"])
        return self.__parse(input)

    def __show_error(self) -> None:
        self.__io.output(self.__messages["error"])

    def __show_success(self) -> None:
        if "success" in self.__messages:
            self.__io.output(self.__messages["success"])


class YesOrNoPrompt(ReapeatingPrompt[YesOrNo]):
    def __init__(self, io: IO, prompt_messages: PromptMessages):
        super().__init__(io, YES_OR_NO_PARSER, prompt_messages)


class BoundedIntPrompt(ReapeatingPrompt[int]):
    def __init__(self, io: IO, valid_range: range, prompt_messages: PromptMessages):
        super().__init__(io, such_that(MULTIFORMAT_INT_PARSER, is_contained_by(valid_range)), prompt_messages)


class NumericStringOfLengthPrompt(ReapeatingPrompt[str]):
    def __init__(self, io: IO, length: int, prompt_messages: PromptMessages):
        parser = such_that(parse_string, has_length(length), all_satisfy(str.isdigit))
        super().__init__(io, parser, prompt_messages)
