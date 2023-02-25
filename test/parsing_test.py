
from parameterized import parameterized  # type: ignore
import unittest

from parsing import MULTIFORMAT_INT_PARSER, YES_OR_NO_PARSER, YesOrNo


class AnyIntParserTest(unittest.TestCase):

    @parameterized.expand([  # type: ignore
        ("1", 1),
        ("0", 0),
        ("-1", -1),
        ("10", 10),
        ("999", 999),
        ("1_0_0_0", 1_0_0_0),
        ("0005", 5)
    ])
    def test_parse_valid_int_in_decimal_format(self, input: str, expected: int):
        result = MULTIFORMAT_INT_PARSER(input)
        self.assertIsNotNone(result)
        self.assertEqual(expected, result)

    @parameterized.expand([  # type: ignore
        ("0b1", 0b1),
        ("0b0", 0b0),
        ("-0b1", -0b1),
        ("0B001", 0b001),
        ("0b111", 0b111),
        ("0B1_1_1_0", 0b1_1_1_0),
        ("0b0001", 0b0001)
    ])
    def test_parse_valid_int_in_binary_format(self, input: str, expected: int):
        result = MULTIFORMAT_INT_PARSER(input)
        self.assertIsNotNone(result)
        self.assertEqual(expected, result)

    @parameterized.expand([  # type: ignore
        ("0x1", 0x1),
        ("ABC", 0xABC),
        ("-0X_1F", -0x_1F),
        ("0b13", 0x0b13),
        ("b13", 0xb13),
        ("0X111", 0x111),
        ("0x1_F_1_F", 0x1_F_1_F),
        ("0x0001", 0x0001),
        ("-1e5", -0x1e5)
    ])
    def test_parse_valid_int_in_hex_format(self, input: str, expected: int):
        result = MULTIFORMAT_INT_PARSER(input)
        self.assertIsNotNone(result)
        self.assertEqual(expected, result)

    @parameterized.expand([  # type: ignore
        ("EFG"),
        ("0x__1"),
        ("0bx1"),
        ("-1-"),
        ("1e-10"),
        ("1.0")
    ])
    def test_not_parse_invalid_int(self, input: str):
        result = MULTIFORMAT_INT_PARSER(input)
        self.assertIsNone(result)


class YesNoParserTest(unittest.TestCase):

    @parameterized.expand([  # type: ignore
        ("YES", YesOrNo.YES),
        ("Yes", YesOrNo.YES),
        ("yeS", YesOrNo.YES),
        ("y", YesOrNo.YES),
        ("NO", YesOrNo.NO),
        ("No", YesOrNo.NO),
        ("nO", YesOrNo.NO),
        ("n", YesOrNo.NO),
    ])
    def test_parse_valid_yes_or_no(self, input: str, expected: YesOrNo):
        result = YES_OR_NO_PARSER(input)
        self.assertIsNotNone(result)
        self.assertEqual(expected, result)
