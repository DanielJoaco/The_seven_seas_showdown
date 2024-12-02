import pygame

class Config:
    def __init__(self, board_size=20):
        # Configuración de la ventana
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1280, 720
        self.CELL_SIZE = 25
        self.BORDER_WIDTH = 1
        self.icon = pygame.image.load("./assets/images/icon.png")
        self.font_bold = "./assets/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf"
        self.font_regular = "./assets/fonts/Pixelify_Sans/static/PixelifySans-Regular.ttf"

        # Colores centralizados
        self.colors = {
            "background": (34, 87, 122),
            "cell": (22, 46, 80),
            "button": (48, 106, 138),
            "hovered_button": (151, 150, 179),
            "selected_cell": (151, 150, 179),
            "border": (0, 0, 0),
            "selected_border": (255, 255, 255),
            "text": (223, 114, 99),
            "water": (105, 105, 105),
            "hit": (229, 88, 18),
            "disabled_button": (128, 128, 128),
            "preview_attack": (151, 150, 179),
            "shielded": (0, 0, 139),  # Usamos el mismo color para celdas protegidas por escudo
        }

        # Configuración del tablero
        self.board_size = board_size
        self.board_x = (self.WINDOW_WIDTH - self.board_size * self.CELL_SIZE) // 2
        self.board_y = (self.WINDOW_HEIGHT - self.board_size * self.CELL_SIZE) // 2

# Instancia global
config = Config()
