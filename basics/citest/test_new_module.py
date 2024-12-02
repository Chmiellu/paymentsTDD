import unittest
from new_module import add, subtract


class TestNewModule(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(7, 3), 10)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)


if __name__ == "__main__":
    unittest.main()
