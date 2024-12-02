import unittest
from tests.test_base import TestBase
from src.modules.player import Player
from src.modules.board import Board

class TestPlayer(TestBase):
    def setUp(self):
        self.board = Board(10)
        self.player = Player("Jugador", self.board)

    def test_initialization(self):
        self.assertEqual(self.player.name, "Jugador")
        self.assertEqual(self.player.life, sum(ship.size for ship in self.player.fleet))
        self.assertEqual(self.player.stamina, 5)
        self.assertFalse(self.player.turn_skipped)
        self.assertFalse(self.player.temp_shield)

    def test_place_ship(self):
        ship = self.player.fleet[0]
        placed = self.player.place_ship(ship, 0, 0, "H")
        self.assertTrue(placed)
        self.assertIn((0, 0), self.player.placed_ships)

    def test_receive_attack_miss(self):
        result = self.player.receive_attack(0, 0)
        self.assertEqual(result, "miss")
        cell = self.board.grid[0][0]
        self.assertEqual(cell["state"], 2)

    def test_receive_attack_hit(self):
        ship = self.player.fleet[0]
        self.player.place_ship(ship, 0, 0, "H")
        result = self.player.receive_attack(0, 0)
        self.assertEqual(result, "hit")
        self.assertEqual(self.player.life, sum(s.size for s in self.player.fleet) - 1)

    def test_receive_attack_shielded(self):
        self.player.temp_shield = True
        result = self.player.receive_attack(0, 0)
        self.assertEqual(result, "shielded")
        self.assertFalse(self.player.temp_shield)

if __name__ == '__main__':
    unittest.main()
