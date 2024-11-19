class Ship:
    def __init__(self, name, size):
        """
        Inicializa un barco con un nombre y tamaño.
        """
        self.name = name
        self.size = size
        self.positions = []

    def place(self, start_pos, orientation, board_size):
        """
        Coloca el barco en el tablero dado un punto de inicio y una orientación.
        """
        self.positions = []
        row, col = start_pos
        for i in range(self.size):
            r = row + (i if orientation == "V" else 0)
            c = col + (i if orientation == "H" else 0)
            if 0 <= r < board_size and 0 <= c < board_size:
                self.positions.append((r, c))
            else:
                raise ValueError("Posición fuera de los límites del tablero.")

def create_fleet():
    """
    Crea una flota basada en definiciones predeterminadas.
    """
    ship_definitions = {
        "Portaaviones": (6, 1),
        "Acorazado": (4, 1),
        "Crucero": (3, 2),
        "Submarino": (2, 3),
        "Destructor": (1, 4),
    }
    fleet = []
    for name, (size, quantity) in ship_definitions.items():
        for _ in range(quantity):
            fleet.append(Ship(name, size))
    return fleet

# Crear una flota global predeterminada
fleet = create_fleet()
