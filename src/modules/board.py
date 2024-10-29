import pygame

def create_board(size):
    board = []
    for _ in range(size):
        row = []
        for _ in range(size):
            row.append(0)
        board.append(row)
    return board

def scale_color(color, scale_factor):
    """Escala el color RGB según un factor, asegurando que los valores estén entre 0 y 255."""
    return tuple(min(255, max(0, int(c * scale_factor))) for c in color)

def show_board(screen, board_created, board_x, board_y, CELL_SIZE, BORDER_COLOR, BORDER_WIDTH, selected_row, selected_col, SELECTED_BORDER_COLOR, cell_color):
    for row in range(len(board_created)):
        for col in range(len(board_created[row])):
            # Calcular las coordenadas de la celda
            cell_x = board_x + col * CELL_SIZE
            cell_y = board_y + row * CELL_SIZE

            # Determinar el color de la celda según su estado
            if board_created[row][col] == 1:  # Barco
                color = cell_color  # Color del barco
            elif board_created[row][col] == 0:  # Agua
                color = scale_color(cell_color, 1.3)  # Color de agua, un tono más claro
            else:  # Barco dañado
                # Ajuste para obtener un color cálido (amarillo-naranja-rojo) basado en `cell_color`
                color = scale_color(cell_color, 0.6) if board_created[row][col] == 2 else scale_color(cell_color, 0.8)

            # Dibujar la celda con su color correspondiente
            pygame.draw.rect(screen, color, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))
            
            # Si la celda es la seleccionada, agregar un borde blanco
            if row == selected_row and col == selected_col:
                pygame.draw.rect(screen, SELECTED_BORDER_COLOR, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), BORDER_WIDTH + 1)
            else:
                # Dibujar el borde estándar en las celdas no seleccionadas
                pygame.draw.rect(screen, BORDER_COLOR, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), BORDER_WIDTH)
