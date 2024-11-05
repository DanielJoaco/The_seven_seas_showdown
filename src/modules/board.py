import pygame
from .config import config

class Board:
    def __init__(self, board_size=20):
        """Inicializa el tablero con el tamaño y la posición centrada en la pantalla."""
        self.cell_size = config.CELL_SIZE  # Tamaño de cada celda en píxeles
        self.board_size = board_size  # Número de celdas por lado (tablero cuadrado)
        
        # Calcular el tamaño en píxeles del tablero y las coordenadas de inicio para centrarlo
        self.pixel_size = self.cell_size * self.board_size
        self.start_x = (config.WINDOW_WIDTH - self.pixel_size) // 2 + self.cell_size
        self.start_y = (config.WINDOW_HEIGHT - self.pixel_size) // 2 + self.cell_size
        
         # Crear la matriz del tablero, donde cada celda es un diccionario
        self.grid = [[{"state": 0, "ship": None} for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        
        # Inicializar la fuente
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, screen):
        """Dibuja el tablero en la pantalla, con colores según el estado de cada celda y etiquetas."""
        # Dibujar etiquetas de columnas (números)
        for col in range(self.board_size):
            number_text = self.font.render(str(col + 1), True, config.text_color)
            number_rect = number_text.get_rect(
                center=(self.start_x + col * self.cell_size + self.cell_size // 2, self.start_y - self.cell_size // 2)
            )
            screen.blit(number_text, number_rect)
        
        # Dibujar etiquetas de filas (letras)
        for row in range(self.board_size):
            letter_text = self.font.render(chr(65 + row), True, config.text_color)
            letter_rect = letter_text.get_rect(
                center=(self.start_x - self.cell_size // 2, self.start_y + row * self.cell_size + self.cell_size // 2)
            )
            screen.blit(letter_text, letter_rect)

        # Dibujar el tablero
        for row in range(self.board_size):
            for col in range(self.board_size):
                # Calcular la posición de cada celda
                x = self.start_x + col * self.cell_size
                y = self.start_y + row * self.cell_size
                
                # Obtener el estado de la celda
                cell = self.grid[row][col]
                cell_state = cell["state"]  # Extraer el estado de la celda
                color = config.cell_color  # Valor predeterminado en caso de estado inesperado

                # Determinar el color según el estado de la celda
                if cell_state == 0:
                    color = config.cell_color  # Celda vacía
                elif cell_state == 1:
                    color = config.selected_cell_color  # Celda con barco
                elif cell_state == 2:
                    color = (105, 105, 105)  # Celda atacada, sin barco (agua)
                elif cell_state == 3:
                    color = (255, 0, 0)  # Celda atacada, con barco (impacto)
                
                # Dibujar la celda con el color correspondiente
                pygame.draw.rect(
                    screen, 
                    color, 
                    pygame.Rect(x, y, self.cell_size, self.cell_size),
                    width=0  # Rellenar la celda
                )
                
                # Dibujar el borde de la celda
                pygame.draw.rect(
                    screen, 
                    config.border_color, 
                    pygame.Rect(x, y, self.cell_size, self.cell_size),
                    width=config.BORDER_WIDTH
                )

    def update_cell(self, row, col, state, ship=None):
        """Actualiza el estado y el identificador de un barco en una celda específica en el tablero."""
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            self.grid[row][col]["state"] = state
            self.grid[row][col]["ship"] = ship
