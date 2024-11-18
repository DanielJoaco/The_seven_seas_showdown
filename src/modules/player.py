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
        self.life = sum(ship.size * ship.quantity for ship in self.fleet)  # Vida basada en las celdas de los barcos
        self.stamina = 5  # Puntos de estamina iniciales
        self.placed_ships = []  # Coordenadas ocupadas por barcos
        self.turn_skipped = False  # Bandera para saltar turno
        self.temp_shield = False  # Bandera para escudo temporal
        self.attack_board = [[{"color": None, "state": 0} for _ in range(board.board_size)] for _ in range(board.board_size)]

    def place_fleet_randomly(self):
        """Coloca toda la flota aleatoriamente en el tablero."""
        orientations = ["H", "V"]
        for ship in self.fleet:
            while True:
                orientation = random.choice(orientations)
                start_row = random.randint(0, self.board.board_size - 1)
                start_col = random.randint(0, self.board.board_size - 1)
                if self.place_ship(ship, start_row, start_col, orientation):
                    break

    def place_ship(self, ship, start_row, start_col, orientation):
        """
        Coloca un barco si la posición es válida. Actualiza el tablero y las posiciones ocupadas.
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
        Verifica si un barco se puede colocar en la posición especificada sin salirse ni colisionar.
        """
        for i in range(ship.size):
            row = start_row + (i if orientation == "V" else 0)
            col = start_col + (i if orientation == "H" else 0)
            
            # Verificar límites del tablero
            if not (0 <= row < self.board.board_size and 0 <= col < self.board.board_size):
                return False

            # Verificar colisiones con otros barcos
            if (row, col) in self.placed_ships:
                return False
        return True

    def receive_attack(self, row, col):
        """
        Recibe un ataque en una posición específica.
        """
        cell = self.board.grid[row][col]
        if cell["state"] == 1:  # Barco impactado
            if self.temp_shield:  # Si el escudo temporal está activo
                self.temp_shield = False
                return "shielded"
            cell["state"] = 3  # Marcar como impactado
            self.life -= 1  # Reducir vida
            return "hit"
        elif cell["state"] == 0:  # Agua
            cell["state"] = 2  # Marcar como fallado
            return "miss"
        return "already_attacked"  # Celda ya atacada

    def attack(self, opponent_board, row, col):
        """
        Realiza un ataque normal.
        """
        return opponent_board.receive_attack(row, col)

    def use_radar(self, opponent_board):
        """
        Usa el radar para detectar la primera celda ocupada por un barco en todo el tablero.
        """
        if self.stamina < 4:
            return "No tienes suficiente estamina para usar el radar."
        
        self.stamina -= 4

        for row in range(opponent_board.board_size):
            for col in range(opponent_board.board_size):
                cell = opponent_board.grid[row][col]
                if cell["state"] == 1:  # Barco encontrado
                    return f"Radar detectó un barco en ({row}, {col})."

        return "No se detectaron barcos en el tablero."

    def add_shield(self, ship):
        """
        Agrega un escudo a un barco específico.
        """
        if self.stamina < 3:
            return "No tienes suficiente estamina para colocar un escudo."
        self.stamina -= 3
        ship.has_shield = True
        return f"Se colocó un escudo en el barco {ship.name}."

    def special_attack(self, opponent_board, row, col, attack_type):
        """
        Realiza un ataque especial.
        - attack_type: Diccionario que incluye el área y el costo de estamina.
        """
        if self.stamina < attack_type["cost"]:
            return f"No tienes suficiente estamina para {attack_type['name']}."
        self.stamina -= attack_type["cost"]
        results = []
        for r in range(row, min(row + attack_type["rows"], opponent_board.board_size)):
            for c in range(col, min(col + attack_type["cols"], opponent_board.board_size)):
                results.append(opponent_board.receive_attack(r, c))
        return results

    def end_turn(self, used_attack):
        """
        Finaliza el turno y actualiza la estamina.
        """
        self.stamina += 2 if used_attack == "normal_attack" else 1
