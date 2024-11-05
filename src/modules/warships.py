class Ship:
    def __init__(self, name, size, quantity):
        """
        Inicializa un barco con un nombre, tamaño (en celdas) y cantidad.
        """
        self.name = name           # Nombre del tipo de barco
        self.size = size           # Tamaño del barco (en número de celdas)
        self.quantity = quantity   # Cantidad de barcos de este tipo
        self.positions = []        # Lista de posiciones de este barco en el tablero (vacía al inicio)

    def place(self, start_pos, orientation):
        """
        Coloca el barco en el tablero dado un punto de inicio y una orientación.
        - start_pos: Tupla (fila, columna) para el inicio del barco.
        - orientation: 'H' para horizontal, 'V' para vertical.
        """
        self.positions = []
        row, col = start_pos
        for i in range(self.size):
            if orientation == 'H':
                self.positions.append((row, col + i))
            elif orientation == 'V':
                self.positions.append((row + i, col))

# Crear una flota de barcos
def create_fleet():
    fleet = [
        Ship("Portaaviones", size=6, quantity=1),    # Tamaño 6, 1 barco
        Ship("Acorazado", size=4, quantity=1),       # Tamaño 4, 1 barco
        Ship("Crucero", size=3, quantity=2),         # Tamaño 3, 2 barcos
        Ship("Submarino", size=2, quantity=3),       # Tamaño 2, 3 barcos
        Ship("Destructor", size=1, quantity=4)       # Tamaño 1, 4 barcos
    ]
    return fleet

# Crear la flota global
fleet = create_fleet()
