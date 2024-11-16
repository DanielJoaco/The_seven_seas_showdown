class Config:
    def __init__(self, board_size=20):
        # Configuración de la ventana
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1280, 720
        self.CELL_SIZE = 25
        self.BORDER_WIDTH = 1

        # Colores centralizados
        self.colors = {
            "background": (34, 87, 122),
            "cell": (53, 172, 120),
            "selected_cell": (199, 249, 204),
            "border": (0, 0, 0),
            "selected_border": (255, 255, 255),
            "text": (229, 88, 18),
            "water": (105, 105, 105),  # Celda atacada sin barco
            "hit": (255, 0, 0),  # Celda atacada con barco
        }

        # Configuración del tablero
        self.board_size = board_size
        self.board_x = (self.WINDOW_WIDTH - self.board_size * self.CELL_SIZE) // 2
        self.board_y = (self.WINDOW_HEIGHT - self.board_size * self.CELL_SIZE) // 2

# Instancia global
config = Config()
