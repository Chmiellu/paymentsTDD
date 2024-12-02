"""
Module to test functions from new_module.

This module uses the unittest framework to test the `add` and `subtract`
functions imported from `new_module`.
"""

import unittest
from new_module import add, subtract  # Upewnij się, że moduł istnieje i zawiera odpowiednie funkcje


class TestNewModule(unittest.TestCase):
    """Test suite for functions in new_module."""

    def test_add(self):
        """Test the add function with positive integers."""
        self.assertEqual(add(7, 3), 10)
        self.assertEqual(add(-2, 5), 3)  # Test case for a negative and positive number
        self.assertEqual(add(0, 0), 0)  # Test case for zeros

    def test_subtract(self):
        """Test the subtract function with positive integers."""
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(3, 5), -2)  # Test case for negative result
        self.assertEqual(subtract(0, 0), 0)  # Test case for zeros


if __name__ == "__main__":
    unittest.main()
