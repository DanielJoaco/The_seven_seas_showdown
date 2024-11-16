import pygame

def is_within_bounds(row, col, board_size):
    """
    Verifica si una celda (row, col) está dentro de los límites del tablero.
    """
    return 0 <= row < board_size and 0 <= col < board_size

def handle_keyboard_navigation(event, selected_row, selected_col, max_row, max_col):
    """
    Maneja la navegación en un tablero o lista usando las teclas de flecha.
    Devuelve las nuevas coordenadas seleccionadas (fila y columna).
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
