from enum import Enum
from typing import Callable, Optional, TypeVar

T = TypeVar("T")
R = TypeVar("R")

Parser = Callable[[T], Optional[R]]
Predicate = Callable[[T], bool]
Function = Callable[[T], R]


class YesOrNo(Enum):
    YES = 'y',
    NO = 'n'


# Common parsers


def parse_yes_or_no(input: str) -> Optional[YesOrNo]:
    return {
        'y': YesOrNo.YES,
        'n': YesOrNo.NO
    }[input]


def parse_int(input: str) -> Optional[int]:
    try:
        return int(input)
    except TypeError:
        return None


def parse_string(input: str) -> Optional[str]:
    return input


# Parser operators


def such_that(parser: Parser[T, R], predicate: Predicate[R]) -> Parser[T, R]:
    return lambda input: satisfying(parser(input), predicate)


def sanitized(parser: Parser[T, R], sanitizer: Function[T, T]) -> Parser[T, R]:
    return lambda input: parser(sanitizer(input))


# Util function that should not be part of API and is here only because of lacking Python features


def satisfying(maybeT: Optional[T], predicate: Predicate[T]) -> Optional[T]:
    return maybeT if maybeT is not None and predicate(maybeT) else None
