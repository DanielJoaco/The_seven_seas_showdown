import pygame
from modules.config import config
from modules.ui import ui

def draw_empty_board(screen, board):
    """
    Dibuja un tablero vacío (sin barcos visibles).
    """
    for row in range(board.board_size):
        for col in range(board.board_size):
            x = board.start_x + col * board.cell_size
            y = board.start_y + row * board.cell_size
            pygame.draw.rect(
                screen, config.colors["cell"], (x, y, board.cell_size, board.cell_size)
            )
            pygame.draw.rect(
                screen,
                config.colors["border"],
                (x, y, board.cell_size, board.cell_size),
                1,
            )

def handle_mouse_selection(event, start_x, start_y, cell_size, board_size):
    """
    Maneja la selección de celdas con el ratón.
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    row = (mouse_y - start_y) // cell_size
    col = (mouse_x - start_x) // cell_size
    if is_within_bounds(row, col, board_size):
        return row, col
    return None, None

def can_place_ship(board, size, start_row, start_col, orientation):
    """
    Verifica si un barco puede ser colocado en la posición indicada.
    """
    for i in range(size):
        row = start_row + (i if orientation == "V" else 0)
        col = start_col + (i if orientation == "H" else 0)
        if not is_within_bounds(row, col, len(board)) or board[row][col]["ship"] is not None or board[row][col]["state"] != 0:
            return False
    return True

def is_within_bounds(row, col, board_size):
    """
    Verifica si una celda (row, col) está dentro de los límites del tablero.
    """
    return 0 <= row < board_size and 0 <= col < board_size

def place_ship_on_board(board, ship, start_row, start_col, orientation):
    """
    Coloca un barco en el tablero.
    """
    for i in range(ship.size):
        row = start_row + (i if orientation == "V" else 0)
        col = start_col + (i if orientation == "H" else 0)
        board.update_cell(row, col, state=1, ship=ship.name)

def handle_navigation_and_selection(event, selected_row, selected_col, board_size, orientation, attack_type, board, screen):
    """
    Maneja la navegación y selección con teclado y mouse en el tablero.
    """
    confirm = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            selected_row = max(0, selected_row - 1)
        elif event.key == pygame.K_DOWN:
            selected_row = min(board_size - 1, selected_row + 1)
        elif event.key == pygame.K_LEFT:
            selected_col = max(0, selected_col - 1)
        elif event.key == pygame.K_RIGHT:
            selected_col = min(board_size - 1, selected_col + 1)
        elif event.key == pygame.K_r and attack_type != "line_attack":
            orientation = toggle_orientation(orientation)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            confirm = True

    elif event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]:
        # Actualizar selección basada en la posición del mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        row = (mouse_y - board.start_y) // board.cell_size
        col = (mouse_x - board.start_x) // board.cell_size
        if is_within_bounds(row, col, board_size):
            selected_row, selected_col = row, col
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                confirm = True

    return selected_row, selected_col, orientation, confirm

def handle_menu_navigation(event, selected_index, num_buttons):
    """
    Maneja la navegación en el menú con teclado.
    """
    confirm = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            selected_index = max(0, selected_index - 1)
        elif event.key == pygame.K_DOWN:
            selected_index = min(num_buttons - 1, selected_index + 1)
        elif event.key == pygame.K_RETURN:
            confirm = True

    return selected_index, confirm

def toggle_orientation(orientation):
    """
    Alterna la orientación entre 'H' y 'V'.
    """
    return "V" if orientation == "H" else "H"

def display_message(screen, message, delay=1000):
    """
    Muestra un mensaje en el área central de la pantalla.
    """
    button_area_width = 400
    button_area_height = 400
    button_area_x = config.WINDOW_WIDTH // 2 - button_area_width // 2
    button_area_y = config.WINDOW_HEIGHT // 2 - button_area_height // 2
    button_area_rect = pygame.Rect(
        button_area_x, button_area_y, button_area_width, button_area_height
    )
    pygame.draw.rect(
        screen, config.colors["background"], button_area_rect, border_radius=10
    )

    font = pygame.font.Font(config.font_regular, 24)
    message_text = font.render(message, True, config.colors["text"])
    message_text_rect = message_text.get_rect(
        center=(button_area_rect.centerx, button_area_rect.centery)
    )
    screen.blit(message_text, message_text_rect)
    ui.update_display()
    pygame.time.delay(delay)
    
def draw_preview(screen, board, selected_row, selected_col, orientation, preview_type="ship", attack_board=None, size=None):
    """
    Dibuja una vista previa de la acción seleccionada.
    """
    if preview_type == 'ship':
        valid = can_place_ship(board.grid, size, selected_row, selected_col, orientation)
        color = config.colors["selected_cell"] if valid else (255, 0, 0)
    else:
        # Para previsualizaciones de ataque
        color = config.colors["preview_attack"]
        size = 1
        valid = True

    positions = []
    if preview_type == "ship":
        # Cálculo de posiciones para colocación de barcos
        positions = [
            (
                selected_row + (i if orientation == "V" else 0),
                selected_col + (i if orientation == "H" else 0),
            )
            for i in range(size)
        ]
    elif preview_type in ["normal_attack", "radar"]:
        # Solo la celda seleccionada
        positions = [(selected_row, selected_col)]
    elif preview_type == "square_attack":
        # Cuadrado de 2x2 celdas
        positions = [
            (selected_row + i, selected_col + j)
            for i in range(2)
            for j in range(2)
        ]
    elif preview_type == "line_attack":
        # Línea de 3 celdas centrada en la celda seleccionada
        positions = []
        offsets = [-1, 0, 1]
        if orientation == "H":
            for offset in offsets:
                col = selected_col + offset
                if is_within_bounds(selected_row, col, board.board_size):
                    positions.append((selected_row, col))
        else:
            for offset in offsets:
                row = selected_row + offset
                if is_within_bounds(row, selected_col, board.board_size):
                    positions.append((row, selected_col))
    else:
        positions = []

    for row, col in positions:
        if is_within_bounds(row, col, board.board_size):
            x = board.start_x + col * board.cell_size
            y = board.start_y + row * board.cell_size

            # Omitir celdas ya atacadas
            if attack_board and attack_board[row][col]["state"] != 0:
                continue

            pygame.draw.rect(
                screen, color, (x, y, board.cell_size, board.cell_size)
            )
            pygame.draw.rect(
                screen,
                config.colors["selected_border"],
                (x, y, board.cell_size, board.cell_size),
                2,
            )