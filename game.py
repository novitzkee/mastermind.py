from abc import ABC, abstractmethod
from random import randint
from typing import TypedDict

from input import BoundedIntPrompt, Console, Prompt, NumericStringOfLengthPrompt, YesOrNoPrompt
from parsing import YesOrNo


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
        return ''.join([str(randint(0, 9)) for _ in range(self.__code_length)])


class SecretCode:
    def __init__(self, code: str) -> None:
        self.__code = code

    def compare(self, attempt: str) -> tuple[int, int]:
        guessed_digits_count = len(
            list(filter(self.__both_equal, zip(attempt, self.__code))))
        
        present_digits_count = len(
            list([digit for digit in attempt if digit in self.__code]))
        
        return (guessed_digits_count, present_digits_count - guessed_digits_count)

    def is_guessed(self, attempt: str) -> bool:
        return all(map(self.__both_equal, zip(attempt, self.__code)))

    def __both_equal(self, pair: tuple[str, str]) -> bool:
        return pair[0] == pair[1]


class GameMessages(TypedDict):
    greeting: str
    instruction: str
    difficulty_warn: str
    ready_ack: str


class Config:
    def __init__(self):
        self.total_tries = 10
        self.code_length = 5
        self.easy_difficulty = False


class ConfigPrompt(Prompt[Config]):
    def __init__(self, game_messages: GameMessages):
        self.__messages = game_messages

        self.__change_code_lenght_prompt = YesOrNoPrompt(
            Console(),
            {
                "ask": "Do You want to change number of digits in generated code? (y/n): ",
                "error": "Yes or No (y/n) ?"
            })

        self.__new_code_length_prompt = BoundedIntPrompt(
            Console(),
            range(1, 11),
            {
                "ask":"Type number of digits in code (1-10): ",
                "error": "Numbers from 1 to 10 are accepted",
            })

        self.__change_num_tries_prompt = YesOrNoPrompt(
            Console(),
            {
                "ask": "Do You want to change number of tries (y/n): ",
                "error": "Yes or No (y/n) ?"
            })
        
        self.__new_num_tries_prompt = BoundedIntPrompt(
            Console(),
            range(1, 21),
            {
                "ask":"Type number of digits in code (1-20): ",
                "error": "Numbers from 1 to 20 are accepted",
            })
        
        self.__change_difficulty_prompt = YesOrNoPrompt(
            Console(),
            {
                "ask": "Do You want to change difficulty level to easy? (y/n): ",
                "error": "Yes or No (y/n) ?",
            })


    def get(self) -> Config:
        config = Config()

        print(self.__messages["greeting"])
        if(self.__change_code_lenght_prompt.get() == YesOrNo.YES):
            config.code_length = self.__new_code_length_prompt.get()

        print(self.__messages["instruction"])
        if(self.__change_num_tries_prompt.get() == YesOrNo.YES):
            config.total_tries = self.__new_num_tries_prompt.get()

        print(self.__messages["difficulty_warn"])
        if(self.__change_difficulty_prompt.get() == YesOrNo.YES):
            config.easy_difficulty = True

        print(self.__messages["ready_ack"])
        return config


class Game:
    def __init__(self, config: Config):
        self.__total_tries = config.total_tries
        self.__current_try = 0

        code_length = config.code_length
        generator = UniqueSymbolsCodeGenerator(code_length) if config.easy_difficulty else RepeatingSymbolsCodeGenerator(code_length)
        self.__secret_code = SecretCode(generator.generate())

        self.__code_attempt_prompt = NumericStringOfLengthPrompt(
            Console(),
            config.code_length,
            {
                "ask": "Type your guess: ",
                "error": f"Please type valid code of length {config.code_length}"
            }
        )

    def play(self):
        while self.__current_try < self.__total_tries:
            self.__current_try += 1

            attempt = self.__code_attempt_prompt.get()
            if(self.__secret_code.is_guessed(attempt)):
                break
            else:
                self.__describe_attempt(attempt)
                     
        if self.__current_try < self.__total_tries:
            print("Congrats you guessed the code!")
        else:
            print("Sorry, you ran out of attempts")
                

    def __describe_attempt(self, attempt: str):
        summary = self.__secret_code.compare(attempt)
        print(f"{summary[0]} {'digit is' if summary[0] == 1 else 'digits are'} correct")
        print(f"{summary[1]} {'digit is' if summary[1] == 1 else 'digits are'} in code")
        print(f"You have {self.__total_tries - self.__current_try} attempts left")
