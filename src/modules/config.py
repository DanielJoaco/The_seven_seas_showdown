class Config:
    def __init__(self, board_size=20):
        # Configuración de la ventana
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 800, 600
        
        # Configuración de tamaño de celda y bordes
        self.CELL_SIZE = 25
        self.BORDER_WIDTH = 1

        # Colores
        self.background_color = (34, 87, 122)
        self.cell_color = (53, 172, 120)
        self.selected_cell_color = (199, 249, 204)
        self.border_color = (0, 0, 0)
        self.selected_border_color = (255,255,255)
        self.text_color = (229, 88, 18)

        # Configuración del tablero
        self.board_size = board_size
        # Centrar el tablero en la ventana
        self.board_x = (self.WINDOW_WIDTH - self.board_size * self.CELL_SIZE) // 2
        self.board_y = (self.WINDOW_HEIGHT - self.board_size * self.CELL_SIZE) // 2

# Crear una instancia global de configuración
config = Config()
