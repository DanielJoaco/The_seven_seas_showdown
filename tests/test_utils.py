import unittest
from tests.test_base import TestBase
from src.modules.utils import is_within_bounds, toggle_orientation

class TestUtils(TestBase):
    def test_is_within_bounds_true(self):
        self.assertTrue(is_within_bounds(5, 5, 10))

    def test_is_within_bounds_false(self):
        self.assertFalse(is_within_bounds(-1, 5, 10))
        self.assertFalse(is_within_bounds(5, 10, 10))

    def test_toggle_orientation(self):
        self.assertEqual(toggle_orientation("H"), "V")
        self.assertEqual(toggle_orientation("V"), "H")

if __name__ == '__main__':
    unittest.main()
