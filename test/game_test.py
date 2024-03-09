from parameterized import parameterized  # type: ignore
import unittest

from game import RepeatingSymbolsCodeGenerator, SecretCode, UniqueSymbolsCodeGenerator


class UniqueSymbolsCodeGeneratorTest(unittest.TestCase):

    @parameterized.expand(map(lambda i: (i,), range(11)))  # type: ignore
    def test_generated_code_contains_unique_digits(self, code_length: int):
        code = UniqueSymbolsCodeGenerator(code_length).generate()

        self.assertEqual(code_length, len(code))
        self.assertEqual(len(code), len(set(code)))
        self.assertTrue(all(map(str.isdigit, code)))


class RepeatingSymbolsCodeGeneratorTest(unittest.TestCase):

    @parameterized.expand(map(lambda i: (i,), range(11)))  # type: ignore
    def test_generated_code_contains_unique_digits(self, code_length: int):
        code = RepeatingSymbolsCodeGenerator(code_length).generate()

        self.assertEqual(code_length, len(code))
        self.assertTrue(all(map(str.isdigit, code)))


class SecretCodeTests(unittest.TestCase):

    @parameterized.expand([ # type: ignore
        ("1", "1", (1, 0)),
        ("123", "123", (3, 0)),
        ("12345", "67890", (0, 0)),
        ("12345", "56789", (0, 1)),
        ("12345", "02040", (2, 0)),
        ("12345", "52143", (2, 3)),
        ("12345", "12354", (3, 2)),
        ("12345", "54321", (1, 4)),
        ("11122", "22111", (1, 4)),
        ("11111", "11112", (4, 0)),
        ("112233", "132132", (3, 3)),
        ("11111", "11111", (5, 0)),
        ("11111", "33133", (1, 0)),
        ("11111", "23456", (0, 0))
    ])
    def test_comparing_attempt_to_code(self, code: str, attempt: str, expected: tuple[int, int]):
        result = SecretCode(code).compare(attempt)

        self.assertEqual(expected, result)


