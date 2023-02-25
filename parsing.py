from enum import Enum
from functools import partial
from typing import Any, Callable, Iterable, Optional, TypeVar

T = TypeVar("T", contravariant=True)
R = TypeVar("R", covariant=True)

Parser = Callable[[T], Optional[R]]
Predicate = Callable[[T], bool]
Function = Callable[[T], R]


class YesOrNo(Enum):
    YES = 'y',
    NO = 'n'


def parse_y_or_n(input: str) -> Optional[YesOrNo]:
    return {
        'y': YesOrNo.YES,
        'n': YesOrNo.NO
    }.get(input)


def parse_yes_or_no(input: str) -> Optional[YesOrNo]:
    return {
        'yes': YesOrNo.YES,
        'no': YesOrNo.NO
    }.get(input)


def parse_int(radix: int, input: str) -> Optional[int]:
    try:
        return int(input, radix)
    except TypeError:
        return None
    except ValueError:
        return None


def parse_string(input: str) -> str:
    return input


# Parser operators


def such_that(parser: Parser[T, R], *predicates: Predicate[R]) -> Parser[T, R]:
    return lambda input: satisfying_all(parser(input), *predicates)


def sanitized(parser: Parser[T, R], sanitizer: Function[T, T]) -> Parser[T, R]:
    return lambda input: parser(sanitizer(input))


def any_of(*parsers: Parser[T, R]) -> Parser[T, R]:
    return lambda input: next(filter(lambda result: result is not None, [parser(input) for parser in parsers]), None)


# Util functions


def satisfying_all(optional: Optional[T], *predicates: Predicate[T]) -> Optional[T]:
    if optional is None:
        return None
    else:
        return optional if all(map(lambda predicate: predicate(optional), predicates)) else None


# Parsers


YES_OR_NO_PARSER = sanitized(any_of(parse_y_or_n, parse_yes_or_no), lambda s: str(s.lower()))


MULTIFORMAT_INT_PARSER = any_of(partial(parse_int, 10), partial(parse_int, 0b10), partial(parse_int, 0x10))


# Validations


def is_contained_by(iterable: Iterable[T]) -> Predicate[T]:
    return lambda input: input in iterable


def has_length(length: int) -> Predicate[Iterable[Any]]:
    return lambda iterable: len(list(iterable)) == length


def all_satisfy(predicate: Predicate[T]) -> Predicate[Iterable[T]]:
    return lambda iterable: all(map(lambda element: predicate(element), iterable))
