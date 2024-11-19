import random
from modules.warships import create_fleet

class Player:
    def __init__(self, name, board):
        """
        Inicializa un jugador con su nombre, tablero, flota, vida y habilidades.
        """
        self.name = name
        self.board = board
        self.fleet = create_fleet()
        self.life = sum(ship.size for ship in self.fleet)
        self.stamina = 5
        self.placed_ships = []
        self.turn_skipped = False
        self.temp_shield = False
        self.attack_board = [
            [{"color": None, "state": 0, "ship": None} for _ in range(board.board_size)]
            for _ in range(board.board_size)
        ]

    def place_fleet_randomly(self):
        """Coloca toda la flota aleatoriamente en el tablero."""
        orientations = ["H", "V"]
        for ship in self.fleet:
            placed = False
            while not placed:
                orientation = random.choice(orientations)
                start_row = random.randint(0, self.board.board_size - 1)
                start_col = random.randint(0, self.board.board_size - 1)
                placed = self.place_ship(ship, start_row, start_col, orientation)

    def place_ship(self, ship, start_row, start_col, orientation):
        """
        Coloca un barco si la posición es válida.
        """
        if not self.can_place_ship(ship, start_row, start_col, orientation):
            return False

        ship.place((start_row, start_col), orientation, self.board.board_size)
        for pos in ship.positions:
            self.placed_ships.append(pos)
            self.board.update_cell(pos[0], pos[1], state=1, ship=ship.name)
        return True

    def can_place_ship(self, ship, start_row, start_col, orientation):
        """
        Verifica si un barco se puede colocar en la posición especificada.
        """
        for i in range(ship.size):
            row = start_row + (i if orientation == "V" else 0)
            col = start_col + (i if orientation == "H" else 0)
            if not (0 <= row < self.board.board_size and 0 <= col < self.board.board_size):
                return False
            if (row, col) in self.placed_ships:
                return False
        return True

    def receive_attack(self, row, col):
        """
        Recibe un ataque en una posición específica.
        """
        cell = self.board.grid[row][col]
        if cell["state"] == 1:
            if self.temp_shield:
                self.temp_shield = False
                return "shielded"
            cell["state"] = 3
            self.life -= 1
            return "hit"
        elif cell["state"] == 0:
            cell["state"] = 2
            return "miss"
        return "already_attacked"

    def attack(self, opponent_board, row, col):
        """
        Realiza un ataque normal.
        """
        return opponent_board.receive_attack(row, col)
