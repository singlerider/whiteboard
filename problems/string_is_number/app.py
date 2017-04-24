#!/usr/bin/env python
import unittest

NUMBER_MAP = set("0123456789")


def string_is_number(input_string):
    """Determines if a given string can be coerced to a number.

    Example numbers: "12", "-46", "1.6", ".76"
    Example non-numbers: "7x", "", "34.", "7.4.3", "-"

    Args:
        input_string (str): The string to evaluate as a number.

    Returns:
        bool: True if input_string can be coerced to a number. False otherwise.
    """
    assert isinstance(input_string, str)

    has_decimal = False

    if len(input_string) < 1:
        return False
    for index, character in enumerate(input_string):
        if character in NUMBER_MAP:
            continue
        if index == 0 and character == "-" and len(input_string) > 1:
            continue
        if character == ".":
            if not has_decimal:
                has_decimal = True
                if index < len(input_string) - 1:
                    continue
        return False
    return True


class StringIsNumberTestCase(unittest.TestCase):

    def test_string_input(self):
        self.assertTrue(string_is_number("12"))
        self.assertTrue(string_is_number("-46"))
        self.assertTrue(string_is_number("1.6"))
        self.assertTrue(string_is_number(".76"))
        self.assertFalse(string_is_number("7x"))
        self.assertFalse(string_is_number(""))
        self.assertFalse(string_is_number("34."))
        self.assertFalse(string_is_number("7.4.3"))
        self.assertFalse(string_is_number("-"))

    def test_non_string_input(self):
        with self.assertRaises(AssertionError):
            string_is_number(None)
        with self.assertRaises(AssertionError):
            string_is_number(15)
        with self.assertRaises(AssertionError):
            string_is_number(13.6)
        with self.assertRaises(AssertionError):
            string_is_number([])

if __name__ == '__main__':
    unittest.main()
