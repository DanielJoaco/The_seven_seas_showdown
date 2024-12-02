import unittest
from tests.test_base import TestBase
from src.modules.board import Board
from src.modules.player import Player
from src.modules.warships import Ship
from src.modules.utils import can_place_ship

class TestGameLogic(TestBase):
    def setUp(self):
        self.board = Board(10)
        self.ship = Ship("Crucero", 3)

    def test_can_place_ship_valid(self):
        result = can_place_ship(self.board.grid, self.ship.size, 0, 0, "H")
        self.assertTrue(result)

    def test_can_place_ship_invalid_out_of_bounds(self):
        result = can_place_ship(self.board.grid, self.ship.size, 0, 8, "H")
        self.assertFalse(result)

    def test_can_place_ship_invalid_overlap(self):
        # Colocar un barco primero
        self.board.update_cell(0, 0, state=1, ship="Submarino")
        result = can_place_ship(self.board.grid, self.ship.size, 0, 0, "H")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
