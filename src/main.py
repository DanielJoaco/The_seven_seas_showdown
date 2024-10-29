import pygame
from modules import *  # Importar todos los módulos del paquete modules

# Inicialización de pygame
pygame.init()

# Dimensiones de la ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Variables de color globales (para que se actualicen en todo el sistema)
background_color = (72, 106, 219)  # Color de fondo
cell_color = (106, 118, 160)       # Color de las celdas
border_color = (58, 51, 48)        # Color del borde de las celdas
selected_border_color = (255, 255, 255)  # Color del borde de la celda seleccionada
CELL_SIZE = 35                     # Tamaño de la celda
BORDER_WIDTH = 1                   # Ancho del borde de la celda

# Crear la ventana
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  

# Crear la matriz tablero
board_created = board.create_board(15)

# Calcular las coordenadas de inicio del tablero para centrarlo
board_width = len(board_created[0]) * CELL_SIZE
board_height = len(board_created) * CELL_SIZE
board_x = (WINDOW_WIDTH - board_width) // 2
board_y = (WINDOW_HEIGHT - board_height) // 2

# Variables para la posición de la celda seleccionada
selected_row = 0
selected_col = 0

# Título del juego
pygame.display.set_caption("The seven seas showdown")

# Control del ciclo principal del juego
clock = pygame.time.Clock()

def start():
    global background_color, cell_color, border_color  # Marcar variables de color como globales
    action = main_menu()
    
    if action == "start_game":
        coordinates = run()
        print("Coordenadas seleccionadas:", coordinates)
    elif action == "show_rules":
        print("Mostrar reglas y cómo se juega")
    elif action == "show_settings":
        result, message = settings.show_settings(screen, WINDOW_WIDTH, WINDOW_HEIGHT, clock)
        if result == "skin_applied":
            print("Skin aplicada:", message)
            # Actualizar los colores globales
            background_color = message[0]
            cell_color = message[1]
            border_color = message[2]
            # Reiniciar el menú para aplicar los cambios visuales
            start()

def main_menu():
    global background_color, cell_color, border_color  # Marcar colores como globales

    # Dimensiones del botón
    button_width = 200
    button_height = 50
    text_color = (255, 255, 255)
    font = pygame.font.Font(None, 36)

    # Posiciones de los botones
    start_button_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 200, button_width, button_height)
    rules_button_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 300, button_width, button_height)
    settings_button_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 400, button_width, button_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    return "start_game"
                elif rules_button_rect.collidepoint(mouse_pos):
                    return "show_rules"
                elif settings_button_rect.collidepoint(mouse_pos):
                    return "show_settings"

        # Rellenar la pantalla con el color de fondo actualizado
        screen.fill(background_color)

        # Dibujar botones con efectos hover usando `cell_color` y `border_color`
        for button_rect, text in [(start_button_rect, "Iniciar Juego"),
                                  (rules_button_rect, "Reglas y Cómo Se Juega"),
                                  (settings_button_rect, "Configuraciones")]:
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, border_color, button_rect)  # Color de borde como hover
            else:
                pygame.draw.rect(screen, cell_color, button_rect)  # Color del botón con `cell_color`

            # Renderizar texto
            text_surface = font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)

def run():
    global selected_row, selected_col, background_color, cell_color, border_color

    running = True
    selected_coordinates = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_row > 0:
                    selected_row -= 1
                elif event.key == pygame.K_DOWN and selected_row < len(board_created) - 1:
                    selected_row += 1
                elif event.key == pygame.K_LEFT and selected_col > 0:
                    selected_col -= 1
                elif event.key == pygame.K_RIGHT and selected_col < len(board_created[0]) - 1:
                    selected_col += 1
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    selected_coordinates = (selected_row, selected_col)
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    start()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = (mouse_x - board_x) // CELL_SIZE
                row = (mouse_y - board_y) // CELL_SIZE
                if 0 <= row < len(board_created) and 0 <= col < len(board_created[0]):
                    selected_row, selected_col = row, col
                    selected_coordinates = (selected_row, selected_col)
                    running = False

        screen.fill(background_color)

        # Dibujar el tablero con los colores actualizados
        board.show_board(screen, board_created, board_x, board_y, CELL_SIZE, border_color, BORDER_WIDTH, selected_row, selected_col, selected_border_color, cell_color)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return selected_coordinates

if __name__ == "__main__":
    start()
