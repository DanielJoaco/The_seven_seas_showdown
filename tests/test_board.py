import unittest
from tests.test_base import TestBase
from src.modules.board import Board

class TestBoard(TestBase):
    def setUp(self):
        self.board_size = 10
        self.board = Board(self.board_size)

    def test_initialization(self):
        self.assertEqual(len(self.board.grid), self.board_size)
        self.assertEqual(len(self.board.grid[0]), self.board_size)
        for row in self.board.grid:
            for cell in row:
                self.assertEqual(cell["state"], 0)
                self.assertIsNone(cell["ship"])

    def test_update_cell(self):
        row, col = 5, 5
        self.board.update_cell(row, col, state=1, ship="Battleship")
        cell = self.board.grid[row][col]
        self.assertEqual(cell["state"], 1)
        self.assertEqual(cell["ship"], "Battleship")

if __name__ == '__main__':
    unittest.main()
