import pygame
from modules.config import config
from modules.utils import is_within_bounds

class Board:
    def __init__(self, board_size=20):
        self.cell_size = config.CELL_SIZE
        self.board_size = board_size
        self.pixel_size = self.cell_size * self.board_size
        self.start_x = config.board_x
        self.start_y = config.board_y
        self.grid = [
            [{"state": 0, "ship": None} for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]
        self.font = pygame.font.Font(config.font_bold, 12)

    def get_cell_color(self, cell):
        """Obtiene el color de una celda basado en su estado."""
        if cell["state"] == 0:
            if cell["ship"]:
                return config.colors["water"]  # Color para barcos no atacados
            else:
                return config.colors["cell"]  # Agua no atacada
        elif cell["state"] == 1:
            return config.colors["ship"]  # Agua atacada (fallo)
        elif cell["state"] == 2:
            return config.colors["water"]  # Barco atacado (impacto)
        elif cell["state"] == 3:
            return config.colors["hit"]  # Barco atacado (impacto)
        elif cell["state"] == 4:
            return config.colors["shielded"]  # Celda protegida por escudo
        else:
            return config.colors["cell"]

    def draw(self, screen):
        """Dibuja el tablero en la pantalla."""
        # Dibujar etiquetas de filas y columnas
        for col in range(self.board_size):
            number_text = self.font.render(str(col + 1), True, config.colors["text"])
            screen.blit(
                number_text,
                (
                    self.start_x + col * self.cell_size + self.cell_size // 2 - number_text.get_width() // 2,
                    self.start_y - self.cell_size // 2 - number_text.get_height() // 2,
                ),
            )
        for row in range(self.board_size):
            letter_text = self.font.render(chr(65 + row), True, config.colors["text"])
            screen.blit(
                letter_text,
                (
                    self.start_x - self.cell_size // 2 - letter_text.get_width() // 2,
                    self.start_y + row * self.cell_size + self.cell_size // 2 - letter_text.get_height() // 2,
                ),
            )

        # Dibujar las celdas del tablero
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = self.start_x + col * self.cell_size
                y = self.start_y + row * self.cell_size
                cell = self.grid[row][col]

                # Determinar el color de la celda
                color = self.get_cell_color(cell)

                # Dibujar la celda
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(x, y, self.cell_size, self.cell_size),
                )
                pygame.draw.rect(
                    screen,
                    config.colors["border"],
                    pygame.Rect(x, y, self.cell_size, self.cell_size),
                    width=config.BORDER_WIDTH,
                )

    def update_cell(self, row, col, state, ship=None):
        """Actualiza el estado de una celda específica en el tablero."""
        if is_within_bounds(row, col, self.board_size):
            self.grid[row][col].update({"state": state, "ship": ship})
