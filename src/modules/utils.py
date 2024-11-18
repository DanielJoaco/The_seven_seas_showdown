import pygame
from modules.config import config

def is_within_bounds(row, col, board_size):
    """
    Verifica si una celda (row, col) está dentro de los límites del tablero.
    """
    return 0 <= row < board_size and 0 <= col < board_size

def handle_navigation_and_selection(event, selected_row, selected_col, board_size, cell_size, start_x, start_y):
    """
    Maneja navegación y selección con teclado y mouse en el tablero.
    """
    if event.type == pygame.KEYDOWN:
        return handle_keyboard_navigation(event, selected_row, selected_col, board_size, board_size)

    elif event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if start_x <= mouse_x < start_x + board_size * cell_size and start_y <= mouse_y < start_y + board_size * cell_size:
            return (mouse_y - start_y) // cell_size, (mouse_x - start_x) // cell_size

    return selected_row, selected_col

def handle_keyboard_navigation(event, selected_row, selected_col, max_row, max_col):
    """
    Maneja la navegación en un tablero o lista usando las teclas de flecha.
    """
    if event.key == pygame.K_UP:
        selected_row = max(0, selected_row - 1)
    elif event.key == pygame.K_DOWN:
        selected_row = min(max_row - 1, selected_row + 1)
    elif event.key == pygame.K_LEFT:
        selected_col = max(0, selected_col - 1)
    elif event.key == pygame.K_RIGHT:
        selected_col = min(max_col - 1, selected_col + 1)
    return selected_row, selected_col

def handle_mouse_selection(event, start_x, start_y, cell_size, board_size):
    """
    Maneja la selección de celdas con el ratón.
    Devuelve las coordenadas de la celda seleccionada (fila, columna) si el ratón está dentro del tablero.
    """
    if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        row = (mouse_y - start_y) // cell_size
        col = (mouse_x - start_x) // cell_size
        if is_within_bounds(row, col, board_size):
            return row, col
    return None

def place_ship_on_board(board, ship, start_row, start_col, orientation):
    """
    Coloca un barco en el tablero.
    """
    for i in range(ship.size):
        row = start_row + (i if orientation == "V" else 0)
        col = start_col + (i if orientation == "H" else 0)
        board.grid[row][col]["state"] = 1
        board.grid[row][col]["ship"] = ship.name

def can_place_ship(board, size, start_row, start_col, orientation):
    """
    Verifica si un barco puede ser colocado en la posición indicada.
    """
    for i in range(size):
        row = start_row + (i if orientation == "V" else 0)
        col = start_col + (i if orientation == "H" else 0)
        if not is_within_bounds(row, col, board.board_size) or board.grid[row][col]["ship"] is not None:
            return False
    return True

def draw_panel(screen, x, y, width, height, info, font):
    """
    Dibuja un panel de información en la pantalla.
    """
    pygame.draw.rect(screen, config.colors["background"], (x, y, width, height), border_radius=10)
    for i, (key, value) in enumerate(info.items()):
        text = font.render(f"{key}: {value}", True, config.colors["text"])
        screen.blit(text, (x + 10, y + 10 + i * 40))

def draw_empty_board(screen, board):
    """
    Dibuja un tablero vacío (sin barcos visibles).
    """
    for row in range(board.board_size):
        for col in range(board.board_size):
            x = board.start_x + col * board.cell_size
            y = board.start_y + row * board.cell_size
            pygame.draw.rect(screen, config.colors["cell"], (x, y, board.cell_size, board.cell_size), 0)
            pygame.draw.rect(screen, config.colors["border"], (x, y, board.cell_size, board.cell_size), 1)
