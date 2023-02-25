
from functools import partial
from parameterized import parameterized  # type: ignore
import unittest

from input import IO, ReapeatingPrompt
from parsing import parse_int, parse_string


class IOMock(IO):
    def __init__(self, inputs: list[str]):
        self.__inputs_iterator = iter(inputs)
        self.prompts: list[str] = []
        self.messages: list[str] = []

    def input(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return next(self.__inputs_iterator)

    def output(self, message: str):
        self.messages.append(message)


class RepeatingPrompterTest(unittest.TestCase):

    def test_returns_input_when_successfully_parsed(self):
        io_mock = IOMock(["Hello world!"])

        prompter = ReapeatingPrompt(io_mock, parse_string, {
            "ask": "ASK",
            "error": "ERROR",
            "success": "SUCCESS"
        })

        result = prompter.get()

        self.assertEqual("Hello world!", result)
        self.assertCountEqual(["ASK"], io_mock.prompts)
        self.assertCountEqual(["SUCCESS"], io_mock.messages)


    def test_reattempt_when_input_failed_to_parse(self):
        io_mock = IOMock(["Not an int", "Not an int again", "1"])

        prompter = ReapeatingPrompt(io_mock, partial(parse_int, 10), {
            "ask": "ASK",
            "error": "ERROR",
            "success": "SUCCESS"
        })

        result = prompter.get()

        self.assertEqual(1, result)
        self.assertCountEqual(["ASK"] * 3, io_mock.prompts)
        self.assertCountEqual(["ERROR"] * 2 + ["SUCCESS"], io_mock.messages)
