import unittest
from tests.test_base import TestBase
from src.modules.board import Board
from src.modules.player import Player
from src.modules.attacks_logic import find_nearest_ship_cell

class TestAttacksLogic(TestBase):
    def setUp(self):
        self.board_size = 10
        self.bot_board = Board(self.board_size)
        self.player_board = Board(self.board_size)
        self.player = Player("Jugador", self.player_board)
        self.bot = Player("Bot", self.bot_board)
        # Colocar un barco en el tablero del bot para las pruebas
        ship = self.bot.fleet[0]
        self.bot.place_ship(ship, 5, 5, "H")

    def test_find_nearest_ship_cell_found(self):
        selected_row, selected_col = 0, 0
        nearest_cell = find_nearest_ship_cell(self.bot_board, selected_row, selected_col, self.player)
        self.assertIsNotNone(nearest_cell)
        self.assertEqual(nearest_cell, (5, 5))

    def test_find_nearest_ship_cell_not_found(self):
        # Eliminar todos los barcos del tablero del bot
        for row in self.bot_board.grid:
            for cell in row:
                cell["ship"] = None
        selected_row, selected_col = 0, 0
        nearest_cell = find_nearest_ship_cell(self.bot_board, selected_row, selected_col, self.player)
        self.assertIsNone(nearest_cell)

if __name__ == '__main__':
    unittest.main()
