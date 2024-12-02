import unittest
from tests.test_base import TestBase
from src.modules.board import Board
from src.modules.player import Player

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

if __name__ == '__main__':
    unittest.main()
