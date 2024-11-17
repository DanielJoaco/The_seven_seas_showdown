import pygame
from .config import config

class Board:
    def __init__(self, board_size=20):
        self.cell_size = config.CELL_SIZE
        self.board_size = board_size
        self.pixel_size = self.cell_size * self.board_size
        self.start_x = config.board_x
        self.start_y = config.board_y
        self.grid = [[{"state": 0, "ship": None} for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.font = pygame.font.Font(config.font_bold, 12)

    def get_cell_color(self, cell_state):
        return config.colors.get(
            {
                0: "cell",
                1: "selected_cell",
                2: "water",
                3: "hit",
            }.get(cell_state, "cell")
        )

    def draw(self, screen, selected_row=None, selected_col=None):
        """Dibuja el tablero en la pantalla y resalta la celda seleccionada."""
        # Dibujar etiquetas de filas y columnas
        for col in range(self.board_size):
            number_text = self.font.render(str(col + 1), True, config.colors["text"])
            screen.blit(number_text, (self.start_x + col * self.cell_size + self.cell_size // 2, self.start_y - self.cell_size // 2))
        for row in range(self.board_size):
            letter_text = self.font.render(chr(65 + row), True, config.colors["text"])
            screen.blit(letter_text, (self.start_x - self.cell_size // 2, self.start_y + row * self.cell_size + self.cell_size // 2))

        # Dibujar las celdas del tablero
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = self.start_x + col * self.cell_size
                y = self.start_y + row * self.cell_size
                cell = self.grid[row][col]

                # Determinar el color de la celda
                color = self.get_cell_color(cell["state"])

                # Si esta celda está seleccionada, aplicar un color especial
                if row == selected_row and col == selected_col:
                    color = config.colors["selected_cell"]

                # Dibujar la celda
                pygame.draw.rect(screen, color, pygame.Rect(x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, config.colors["border"], pygame.Rect(x, y, self.cell_size, self.cell_size), width=config.BORDER_WIDTH)

    def update_cell(self, row, col, state, ship=None):
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            self.grid[row][col]["state"] = state
            self.grid[row][col]["ship"] = ship
