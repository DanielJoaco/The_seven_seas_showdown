class Ship:
    def __init__(self, name, size, quantity):
        """
        Inicializa un barco con un nombre, tamaño (en celdas) y cantidad.
        """
        self.name = name           # Nombre del tipo de barco
        self.size = size           # Tamaño del barco (en número de celdas)
        self.quantity = quantity   # Cantidad de barcos de este tipo
        self.positions = []        # Lista de posiciones de este barco en el tablero (vacía al inicio)

    def place(self, start_pos, orientation, board_size):
        """
        Coloca el barco en el tablero dado un punto de inicio y una orientación.
        - start_pos: Tupla (fila, columna) para el inicio del barco.
        - orientation: 'H' para horizontal, 'V' para vertical.
        - board_size: Tamaño del tablero (para validar límites).
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

# Crear una flota de barcos
def create_fleet(ship_definitions=None):
    """
    Crea una flota basada en definiciones proporcionadas o utiliza valores predeterminados.
    - ship_definitions: Diccionario opcional con {nombre: (tamaño, cantidad)}.
    """
    if ship_definitions is None:
        ship_definitions = {
            "Portaaviones": (6, 1),  # Tamaño 6, 1 barco
            "Acorazado": (4, 1),    # Tamaño 4, 1 barco
            "Crucero": (3, 2),      # Tamaño 3, 2 barcos
            "Submarino": (2, 3),    # Tamaño 2, 3 barcos
            "Destructor": (1, 4),   # Tamaño 1, 4 barcos
        }
    # Crear la lista de barcos desglosada por cantidad
    fleet = []
    for name, (size, quantity) in ship_definitions.items():
        for _ in range(quantity):
            fleet.append(Ship(name, size, 1))  # Cada barco individual tiene cantidad 1
    return fleet


# Crear una flota global predeterminada
fleet = create_fleet()
