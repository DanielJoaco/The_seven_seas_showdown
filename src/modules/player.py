import random
from .warships import create_fleet

class Player:
    def __init__(self, name, board):
        """
        Inicializa un jugador con su nombre, tablero, flota, vida y habilidades.
        """
        self.name = name
        self.board = board
        self.fleet = create_fleet()  # Crear la flota de barcos del jugador
        self.life = sum(ship.size * ship.quantity for ship in self.fleet)  # Vida basada en el total de celdas de barcos
        self.stamina = 5  # Puntos de estamina iniciales para habilidades especiales
        self.shields = 2  # Número de escudos disponibles
        self.radar = 1    # Uso de radar disponible
        self.placed_ships = []  # Posiciones de barcos ya colocados para evitar colisiones

    def can_place_ship(self, ship, start_row, start_col, orientation):
        """Verifica si un barco se puede colocar en la posición especificada sin salirse ni colisionar."""
        for i in range(ship.size):
            row = start_row + (i if orientation == "V" else 0)
            col = start_col + (i if orientation == "H" else 0)
            
            # Verificar límites del tablero
            if row >= self.board.board_size or col >= self.board.board_size or row < 0 or col < 0:
                return False

            # Verificar colisiones con otros barcos
            if (row, col) in self.placed_ships:
                return False
        return True

    def place_ship(self, ship, start_row, start_col, orientation):
        """Coloca el barco si es una posición válida y actualiza las celdas ocupadas con su identificador."""
        if not self.can_place_ship(ship, start_row, start_col, orientation):
            return False

        ship.place((start_row, start_col), orientation)
        for pos in ship.positions:
            self.placed_ships.append(pos)
            self.board.update_cell(pos[0], pos[1], state=1, ship=ship.name)  # Actualizamos también el nombre del barco
        return True

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

    def attack(self, opponent_board, row, col):
        """
        Realiza un ataque en el tablero del oponente y devuelve el resultado.
        """
        result = opponent_board.receive_attack(row, col)
        if result == "hit":
            self.stamina += 1  # Ganar estamina al acertar
        return result

    def special_attack_square(self, opponent_board, row, col):
        """
        Realiza un ataque especial en un área de 2x2 celdas.
        """
        if self.stamina < 2:
            print("No tienes suficiente estamina para un ataque especial.")
            return None
        self.stamina -= 2  # Consumir estamina por usar ataque especial
        print(f"{self.name} realiza un ataque especial en cuadrado!")
        results = []
        for r in range(row, min(row + 2, opponent_board.board_size)):
            for c in range(col, min(col + 2, opponent_board.board_size)):
                result = opponent_board.receive_attack(r, c)
                results.append((r, c, result))
        return results

    def special_attack_line(self, opponent_board, row, col, orientation="horizontal"):
        """
        Realiza un ataque especial en una línea de 3 celdas.
        """
        if self.stamina < 3:
            print("No tienes suficiente estamina para un ataque en línea.")
            return None
        self.stamina -= 3  # Consumir estamina por usar ataque en línea
        print(f"{self.name} realiza un ataque especial en línea!")
        results = []
        for i in range(3):
            r, c = (row, col + i) if orientation == "horizontal" else (row + i, col)
            if r < opponent_board.board_size and c < opponent_board.board_size:
                result = opponent_board.receive_attack(r, c)
                results.append((r, c, result))
        return results

    def use_radar(self, opponent_board, row, col):
        """
        Usa el radar para detectar barcos en un área de 3x3 alrededor de la coordenada dada.
        """
        if self.radar <= 0:
            print("No tienes uso de radar disponible.")
            return None
        self.radar -= 1  # Consumir un uso de radar
        print(f"{self.name} usa el radar en el área de ({row},{col})!")
        for r in range(max(0, row - 1), min(row + 2, opponent_board.board_size)):
            for c in range(max(0, col - 1), min(col + 2, opponent_board.board_size)):
                if opponent_board.grid[r][c] == 1:  # Barco encontrado
                    print(f"Radar detectó un barco en ({r}, {c})!")
                    return r, c
        print("No se detectaron barcos en el área.")
        return None  # No se encontró ningún barco

    def receive_attack(self, row, col):
        """
        Recibe un ataque en una posición específica del tablero del jugador.
        Devuelve "hit" si impacta un barco, "miss" si no hay barco, o "already_attacked" si ya fue atacado.
        """
        cell = self.board.grid[row][col]
        if cell["state"] == 1:  # Si hay un barco sin dañar
            cell["state"] = 3  # Marcar como impactado
            self.life -= 1  # Reducir la vida del jugador
            return "hit"
        elif cell["state"] == 0:  # Si es agua
            cell["state"] = 2  # Marcar como fallado
            return "miss"
        return "already_attacked"  # Si ya fue atacado previamente

