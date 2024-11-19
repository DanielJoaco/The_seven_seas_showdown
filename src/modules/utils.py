import pygame
from modules.config import config

def draw_panel(screen, x, y, width, height, info, font):
    """
    Dibuja un panel de información en la pantalla.

    :param screen: Superficie de Pygame para dibujar.
    :param x: Coordenada x de la esquina superior izquierda del panel.
    :param y: Coordenada y de la esquina superior izquierda del panel.
    :param width: Ancho del panel.
    :param height: Altura del panel.
    :param info: Diccionario con la información a mostrar (clave: valor).
    :param font: Fuente de Pygame para renderizar el texto.
    """
    # Dibujar el fondo del panel
    pygame.draw.rect(screen, config.colors["background"], (x, y, width, height), border_radius=10)
    
    # Dibujar un borde alrededor del panel
    pygame.draw.rect(screen, config.colors["border"], (x, y, width, height), 2, border_radius=10)
    
    # Renderizar y dibujar cada línea de información
    padding = 10
    line_height = 30
    for i, (key, value) in enumerate(info.items()):
        text = font.render(f"{key}: {value}", True, config.colors["text"])
        screen.blit(text, (x + padding, y + padding + i * line_height))


def draw_empty_board(screen, board):
    """
    Dibuja un tablero vacío (sin barcos visibles).

    :param screen: Superficie de Pygame para dibujar.
    :param board: Objeto del tablero que contiene las propiedades necesarias.
    """
    for row in range(board.board_size):
        for col in range(board.board_size):
            x = board.start_x + col * board.cell_size
            y = board.start_y + row * board.cell_size
            
            # Dibujar la celda del tablero
            pygame.draw.rect(screen, config.colors["cell"], (x, y, board.cell_size, board.cell_size))
            
            # Dibujar el borde de la celda
            pygame.draw.rect(screen, config.colors["border"], (x, y, board.cell_size, board.cell_size), 1)

def is_within_bounds(row, col, board_size):
    """
    Verifica si una celda (row, col) está dentro de los límites del tablero.
    """
    return 0 <= row < board_size and 0 <= col < board_size


def handle_mouse_selection(event, start_x, start_y, cell_size, board_size):
    """
    Maneja la selección de celdas con el ratón.
    Devuelve las coordenadas de la celda seleccionada (fila, columna) si el ratón está dentro del tablero.
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
        if not is_within_bounds(row, col, board.board_size) or board.grid[row][col]["ship"] is not None:
            return False
    return True


def place_ship_on_board(board, ship, start_row, start_col, orientation):
    """
    Coloca un barco en el tablero.
    """
    for i in range(ship.size):
        row = start_row + (i if orientation == "V" else 0)
        col = start_col + (i if orientation == "H" else 0)
        board.grid[row][col]["state"] = 1
        board.grid[row][col]["ship"] = ship.name


def handle_navigation_and_selection(event, selected_row, selected_col, board_size, orientation, attack_type, board, screen):
    """
    Maneja la navegación y selección con teclado y mouse en el tablero.
    
    :param event: Evento de Pygame.
    :param selected_row: Fila actualmente seleccionada.
    :param selected_col: Columna actualmente seleccionada.
    :param board_size: Tamaño del tablero.
    :param orientation: Orientación actual ('H' o 'V').
    :param attack_type: Tipo de ataque ("normal_attack", "line_attack", "square_attack") o None.
    :param board: Objeto del tablero.
    :param screen: Superficie de Pygame para dibujar.
    :return: (fila, columna, orientación, confirmación)
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
            if attack_type == "square_attack":
                if not is_within_bounds(selected_row + 1, selected_col + 1, board_size):
                    display_message(screen, "Ataque fuera de los límites.")
                else:
                    confirm = True
            else:
                confirm = True

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        row, col = handle_mouse_selection(
            event, board.start_x, board.start_y, board.cell_size, board.board_size
        )
        if row is not None and col is not None:
            if attack_type == "square_attack":
                if not is_within_bounds(row + 1, col + 1, board_size):
                    display_message(screen, "Ataque cuadrado fuera de los límites.")
                else:
                    selected_row, selected_col = row, col
                    confirm = True
            else:
                selected_row, selected_col = row, col
                confirm = True

    return selected_row, selected_col, orientation, confirm


def handle_menu_navigation(event, selected_index, num_buttons):
    """
    Maneja la navegación en el menú con teclado.

    :param event: Evento de Pygame.
    :param selected_index: Índice actualmente seleccionado.
    :param num_buttons: Número total de botones en el menú.
    :return: (nuevo índice seleccionado, confirmación)
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

    :param orientation: Orientación actual ('H' o 'V').
    :return: Nueva orientación.
    """
    return "V" if orientation == "H" else "H"


def display_message(screen, message):
    """
    Muestra un mensaje en el área central de la pantalla.
    
    :param screen: Superficie de Pygame para dibujar.
    :param message: Texto del mensaje a mostrar.
    """
    button_area_width = 300
    button_area_height = 150
    button_area_x = config.WINDOW_WIDTH // 2 - button_area_width // 2
    button_area_y = config.WINDOW_HEIGHT // 2 - button_area_height // 2
    button_area_rect = pygame.Rect(button_area_x, button_area_y, button_area_width, button_area_height)

    # Dibujar el fondo del mensaje
    pygame.draw.rect(screen, config.colors["background"], button_area_rect, border_radius=10)
    pygame.draw.rect(screen, config.colors["border"], button_area_rect, width=4, border_radius=10)

    # Renderizar el texto del mensaje
    font = pygame.font.Font(config.font_regular, 24)
    message_text = font.render(message, True, config.colors["text"])
    message_text_rect = message_text.get_rect(center=(button_area_rect.centerx, button_area_rect.centery))
    screen.blit(message_text, message_text_rect)
    
    # Actualizar la pantalla para mostrar el mensaje
    pygame.display.flip()
    pygame.time.delay(1500)  # Mostrar el mensaje durante 1.5 segundos


def draw_preview(screen, board, selected_row, selected_col, size, orientation, preview_type="ship"):
    """
    Dibuja una vista previa de la acción seleccionada.

    :param screen: Superficie de Pygame para dibujar.
    :param board: Tablero donde se dibuja.
    :param selected_row: Fila seleccionada.
    :param selected_col: Columna seleccionada.
    :param size: Tamaño del objeto a previsualizar.
    :param orientation: Orientación ('H' o 'V').
    :param preview_type: Tipo de previsualización ('ship', 'attack_normal', 'attack_square', 'attack_line').
    """
    if preview_type == 'ship':
        valid = can_place_ship(board, size, selected_row, selected_col, orientation)
        color = config.colors["selected_cell"] if valid else (255, 0, 0)
    else:
        # Para previsualizaciones de ataque
        color = config.colors["selected_cell"]

    if preview_type == "ship" or preview_type == "attack_normal":
        for i in range(size):
            row = selected_row + (i if orientation == "V" else 0)
            col = selected_col + (i if orientation == "H" else 0)
            if is_within_bounds(row, col, board.board_size):
                x = board.start_x + col * board.cell_size
                y = board.start_y + row * board.cell_size
                pygame.draw.rect(screen, color, (x, y, board.cell_size, board.cell_size), 0)
                pygame.draw.rect(screen, config.colors["selected_border"], (x, y, board.cell_size, board.cell_size), 2)
    elif preview_type == "attack_square":
        for i in range(2):
            for j in range(2):
                r = selected_row + i
                c = selected_col + j
                if is_within_bounds(r, c, board.board_size):
                    x = board.start_x + c * board.cell_size
                    y = board.start_y + r * board.cell_size
                    pygame.draw.rect(screen, color, (x, y, board.cell_size, board.cell_size), 0)
                    pygame.draw.rect(screen, config.colors["selected_border"], (x, y, board.cell_size, board.cell_size), 2)
    elif preview_type == "attack_line":
        if orientation == "H":
            for c in range(board.board_size):
                x = board.start_x + c * board.cell_size
                y = board.start_y + selected_row * board.cell_size
                pygame.draw.rect(screen, color, (x, y, board.cell_size, board.cell_size), 0)
                pygame.draw.rect(screen, config.colors["selected_border"], (x, y, board.cell_size, board.cell_size), 2)
        else:
            for r in range(board.board_size):
                x = board.start_x + selected_col * board.cell_size
                y = board.start_y + r * board.cell_size
                pygame.draw.rect(screen, color, (x, y, board.cell_size, board.cell_size), 0)
                pygame.draw.rect(screen, config.colors["selected_border"], (x, y, board.cell_size, board.cell_size), 2)
