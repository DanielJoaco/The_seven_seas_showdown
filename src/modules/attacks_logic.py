# modules/attacks_logic.py

import pygame
from modules.config import config
from modules.utils import (
    is_within_bounds,
    handle_mouse_selection,
    draw_panel,
    draw_empty_board,
)
from modules.ui import ui  # Importar la instancia ui
from modules.buttons import is_mouse_over_button, draw_button
from modules.utils import display_message  # Asegúrate de tener esta función en game_logic.py


def handle_attack_action(screen, player, bot, bot_board, attack_type):
    """
    Maneja la lógica para los diferentes tipos de ataques.

    :param screen: Superficie de Pygame para dibujar.
    :param player: Jugador que realiza el ataque.
    :param bot: Bot que recibe el ataque.
    :param bot_board: Tablero del bot.
    :param attack_type: Tipo de ataque ("normal_attack", "line_attack", "square_attack").
    :return: Nuevo estado del turno.
    """
    if attack_type == "normal_attack":
        return handle_normal_attack(screen, player, bot, bot_board)
    elif attack_type == "line_attack":
        return handle_line_attack(screen, player, bot, bot_board)
    elif attack_type == "square_attack":
        return handle_square_attack(screen, player, bot, bot_board)
    else:
        print(f"Tipo de ataque desconocido: {attack_type}")
        return "player_turn"


def handle_normal_attack(screen, player, bot, bot_board):
    """
    Maneja un ataque normal.

    :param screen: Superficie de Pygame para dibujar.
    :param player: Jugador que realiza el ataque.
    :param bot: Bot que recibe el ataque.
    :param bot_board: Tablero del bot.
    :return: Nuevo estado del turno.
    """
    selected_row, selected_col = select_attack_cell(screen, bot_board, player, bot, attack_type="normal")
    if selected_row is None or selected_col is None:
        return "player_turn"

    # Verificar si la celda ya ha sido atacada
    if player.attack_board[selected_row][selected_col]["state"] != 0:
        display_message(screen, "Esta celda ya ha sido atacada.")
        return "player_turn"

    # Realizar el ataque
    result = bot_board.receive_attack(selected_row, selected_col)
    update_attack_board(player, selected_row, selected_col, result)

    # Actualizar el tablero de ataque visualmente
    update_bot_attack_board_visual(screen, player, bot_board)

    # Dibujar el estado actualizado
    ui.draw_game_state(screen, player, bot, None, bot_board, "player_turn_attack", 0)
    ui.update_display()

    if result == "hit":
        display_message(screen, "¡Impacto!")
        return "player_turn_attack"  # Permitir otro ataque normal
    elif result == "miss":
        display_message(screen, "Fallo.")
        return "bot_turn"
    elif result == "already_attacked":
        display_message(screen, "La celda ya fue atacada.")
        return "player_turn"


def handle_line_attack(screen, player, bot, bot_board):
    """
    Maneja un ataque lineal.

    :param screen: Superficie de Pygame para dibujar.
    :param player: Jugador que realiza el ataque.
    :param bot: Bot que recibe el ataque.
    :param bot_board: Tablero del bot.
    :return: Nuevo estado del turno.
    """
    selected_row, selected_col, orientation = select_attack_line(screen, bot_board, player, bot)
    if selected_row is None or selected_col is None or orientation is None:
        return "player_turn"

    # Determinar las celdas a atacar en línea
    cells_to_attack = []
    if orientation == "H":
        for c in range(bot_board.board_size):
            cells_to_attack.append((selected_row, c))
    else:  # "V"
        for r in range(bot_board.board_size):
            cells_to_attack.append((r, selected_col))

    # Realizar ataques
    any_hit = False
    for row, col in cells_to_attack:
        if player.attack_board[row][col]["state"] == 0:
            result = bot_board.receive_attack(row, col)
            update_attack_board(player, row, col, result)
            if result == "hit":
                any_hit = True

    # Actualizar el tablero de ataque visualmente
    update_bot_attack_board_visual(screen, player, bot_board)

    # Dibujar el estado actualizado
    ui.draw_game_state(screen, player, bot, None, bot_board, "player_turn_attack", 0)
    ui.update_display()

    if any_hit:
        display_message(screen, "¡Impacto en la línea!")
        return "player_turn_attack"  # Permitir otro ataque normal
    else:
        display_message(screen, "Ataque lineal fallido.")
        return "bot_turn"


def handle_square_attack(screen, player, bot, bot_board):
    """
    Maneja un ataque cuadrado.

    :param screen: Superficie de Pygame para dibujar.
    :param player: Jugador que realiza el ataque.
    :param bot: Bot que recibe el ataque.
    :param bot_board: Tablero del bot.
    :return: Nuevo estado del turno.
    """
    selected_row, selected_col = select_attack_cell(screen, bot_board, player, bot, attack_type="square")
    if selected_row is None or selected_col is None:
        return "player_turn"

    # Determinar las celdas en el área 2x2
    cells_to_attack = [
        (selected_row, selected_col),
        (selected_row, selected_col + 1),
        (selected_row + 1, selected_col),
        (selected_row + 1, selected_col + 1),
    ]

    # Filtrar celdas fuera de los límites
    cells_to_attack = [
        (r, c) for r, c in cells_to_attack
        if is_within_bounds(r, c, bot_board.board_size)
    ]

    # Realizar ataques
    any_hit = False
    for row, col in cells_to_attack:
        if player.attack_board[row][col]["state"] == 0:
            result = bot_board.receive_attack(row, col)
            update_attack_board(player, row, col, result)
            if result == "hit":
                any_hit = True

    # Actualizar el tablero de ataque visualmente
    update_bot_attack_board_visual(screen, player, bot_board)

    # Dibujar el estado actualizado
    ui.draw_game_state(screen, player, bot, None, bot_board, "player_turn_attack", 0)
    ui.update_display()

    if any_hit:
        display_message(screen, "¡Impacto en el área!")
        return "player_turn_attack"  # Permitir otro ataque normal
    else:
        display_message(screen, "Ataque cuadrado fallido.")
        return "bot_turn"


def select_attack_cell(screen, bot_board, player, bot, attack_type="normal"):
    """
    Permite al jugador seleccionar una celda objetivo en el tablero del bot.
    Similar a la colocación de barcos.

    :param screen: Superficie de Pygame para dibujar.
    :param bot_board: Tablero del bot.
    :param player: Jugador que realiza el ataque.
    :param bot: Bot que recibe el ataque.
    :param attack_type: Tipo de ataque ("normal", "square").
    :return: (fila, columna) seleccionadas o (None, None) si se cancela.
    """
    selected_row, selected_col = 0, 0
    orientation = "H"  # Predeterminado (solo relevante para ciertos ataques)
    clock = pygame.time.Clock()

    while True:
        screen.fill(config.colors["background"])
        ui.draw_game_state(screen, player, bot, None, bot_board, "attack_selection", 0)
        draw_attack_preview(screen, bot_board, selected_row, selected_col, orientation, attack_type)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Navegación con teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_row = max(0, selected_row - 1)
                elif event.key == pygame.K_DOWN:
                    selected_row = min(bot_board.board_size - 1, selected_row + 1)
                elif event.key == pygame.K_LEFT:
                    selected_col = max(0, selected_col - 1)
                elif event.key == pygame.K_RIGHT:
                    selected_col = min(bot_board.board_size - 1, selected_col + 1)
                elif event.key == pygame.K_r and attack_type != "line_attack":
                    orientation = "V" if orientation == "H" else "H"
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    # Validar la posición antes de retornar
                    if attack_type == "square":
                        if not is_within_bounds(selected_row + 1, selected_col + 1, bot_board.board_size):
                            display_message(screen, "Ataque fuera de los límites.")
                            continue
                    return selected_row, selected_col

            # Selección con mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if is_mouse_over_board(mouse_x, mouse_y, bot_board):
                    row, col = handle_mouse_selection(
                        event, bot_board.start_x, bot_board.start_y, bot_board.cell_size, bot_board.board_size
                    )
                    if row is not None and col is not None:
                        if attack_type == "square":
                            # Verificar límites para ataques cuadrados
                            if not is_within_bounds(row + 1, col + 1, bot_board.board_size):
                                display_message(screen, "Ataque cuadrado fuera de los límites.")
                                continue
                        return row, col

        clock.tick(60)


def select_attack_line(screen, bot_board, player, bot):
    """
    Permite al jugador seleccionar una fila o columna para un ataque lineal.

    :param screen: Superficie de Pygame para dibujar.
    :param bot_board: Tablero del bot.
    :param player: Jugador que realiza el ataque.
    :param bot: Bot que recibe el ataque.
    :return: (fila, columna, orientación) seleccionadas o (None, None, None) si se cancela.
    """
    selected_row, selected_col = 0, 0
    orientation = "H"  # Predeterminado
    clock = pygame.time.Clock()

    while True:
        screen.fill(config.colors["background"])
        ui.draw_game_state(screen, player, bot, None, bot_board, "attack_selection", 0)
        draw_line_attack_preview(screen, bot_board, selected_row, selected_col, orientation)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Navegación con teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_row = max(0, selected_row - 1)
                elif event.key == pygame.K_DOWN:
                    selected_row = min(bot_board.board_size - 1, selected_row + 1)
                elif event.key == pygame.K_LEFT:
                    selected_col = max(0, selected_col - 1)
                elif event.key == pygame.K_RIGHT:
                    selected_col = min(bot_board.board_size - 1, selected_col + 1)
                elif event.key == pygame.K_r:
                    orientation = "V" if orientation == "H" else "H"
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return selected_row, selected_col, orientation

            # Selección con mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if is_mouse_over_board(mouse_x, mouse_y, bot_board):
                    row, col = handle_mouse_selection(
                        event, bot_board.start_x, bot_board.start_y, bot_board.cell_size, bot_board.board_size
                    )
                    if row is not None and col is not None:
                        # Verificar límites para ataques lineales
                        if orientation == "H":
                            if not is_within_bounds(row, bot_board.board_size - 1, bot_board.board_size):
                                display_message(screen, "Ataque lineal horizontal fuera de los límites.")
                                continue
                        else:
                            if not is_within_bounds(bot_board.board_size - 1, col, bot_board.board_size):
                                display_message(screen, "Ataque lineal vertical fuera de los límites.")
                                continue
                        return row, col, orientation

        clock.tick(60)


def update_attack_board(player, row, col, result):
    """
    Actualiza el tablero de ataque del jugador basado en el resultado del ataque.

    :param player: Jugador que realiza el ataque.
    :param row: Fila atacada.
    :param col: Columna atacada.
    :param result: Resultado del ataque ("hit", "miss").
    """
    if result == "hit":
        player.attack_board[row][col]["state"] = 2  # Impacto
        player.attack_board[row][col]["color"] = config.colors["hit"]
    elif result == "miss":
        player.attack_board[row][col]["state"] = 1  # Agua
        player.attack_board[row][col]["color"] = config.colors["water"]


def update_bot_attack_board_visual(screen, player, bot_board):
    """
    Dibuja el tablero de ataque del bot con las celdas atacadas.

    :param screen: Superficie de Pygame para dibujar.
    :param player: Jugador que realiza el ataque.
    :param bot_board: Tablero del bot.
    """
    for row in range(bot_board.board_size):
        for col in range(bot_board.board_size):
            attack_state = player.attack_board[row][col]["state"]
            color = player.attack_board[row][col]["color"]
            if attack_state != 0:
                x = bot_board.start_x + col * bot_board.cell_size
                y = bot_board.start_y + row * bot_board.cell_size
                pygame.draw.rect(screen, color, (x, y, bot_board.cell_size, bot_board.cell_size))
                pygame.draw.rect(screen, config.colors["border"], (x, y, bot_board.cell_size, bot_board.cell_size), width=config.BORDER_WIDTH)


def draw_attack_preview(screen, bot_board, row, col, orientation, attack_type="normal"):
    """
    Dibuja una vista previa del ataque en la posición seleccionada.

    :param screen: Superficie de Pygame para dibujar.
    :param bot_board: Tablero del bot.
    :param row: Fila seleccionada.
    :param col: Columna seleccionada.
    :param orientation: Orientación del ataque ("H" o "V").
    :param attack_type: Tipo de ataque ("normal", "square", "line").
    """
    color = config.colors["selected_cell"]

    if attack_type == "normal":
        # Solo una celda
        if is_within_bounds(row, col, bot_board.board_size):
            x = bot_board.start_x + col * bot_board.cell_size
            y = bot_board.start_y + row * bot_board.cell_size
            pygame.draw.rect(screen, color, (x, y, bot_board.cell_size, bot_board.cell_size), 0)
            pygame.draw.rect(screen, config.colors["selected_border"], (x, y, bot_board.cell_size, bot_board.cell_size), 2)
    elif attack_type == "square":
        # Área 2x2
        for i in range(2):
            for j in range(2):
                r = row + i
                c = col + j
                if is_within_bounds(r, c, bot_board.board_size):
                    x = bot_board.start_x + c * bot_board.cell_size
                    y = bot_board.start_y + r * bot_board.cell_size
                    pygame.draw.rect(screen, color, (x, y, bot_board.cell_size, bot_board.cell_size), 0)
                    pygame.draw.rect(screen, config.colors["selected_border"], (x, y, bot_board.cell_size, bot_board.cell_size), 2)
    elif attack_type == "line":
        # Línea horizontal o vertical
        if orientation == "H":
            for c in range(bot_board.board_size):
                x = bot_board.start_x + c * bot_board.cell_size
                y = bot_board.start_y + row * bot_board.cell_size
                pygame.draw.rect(screen, color, (x, y, bot_board.cell_size, bot_board.cell_size), 0)
                pygame.draw.rect(screen, config.colors["selected_border"], (x, y, bot_board.cell_size, bot_board.cell_size), 2)
        else:
            for r in range(bot_board.board_size):
                x = bot_board.start_x + col * bot_board.cell_size
                y = bot_board.start_y + r * bot_board.cell_size
                pygame.draw.rect(screen, color, (x, y, bot_board.cell_size, bot_board.cell_size), 0)
                pygame.draw.rect(screen, config.colors["selected_border"], (x, y, bot_board.cell_size, bot_board.cell_size), 2)


def draw_line_attack_preview(screen, bot_board, row, col, orientation):
    """
    Dibuja una vista previa del ataque lineal.

    :param screen: Superficie de Pygame para dibujar.
    :param bot_board: Tablero del bot.
    :param row: Fila seleccionada.
    :param col: Columna seleccionada.
    :param orientation: Orientación del ataque ("H" o "V").
    """
    draw_attack_preview(screen, bot_board, row, col, orientation, attack_type="line")


def display_message(screen, message):
    """
    Muestra un mensaje en el área central.

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
    ui.update_display()
    pygame.time.delay(1500)  # Mostrar el mensaje durante 1.5 segundos


def is_mouse_over_board(mouse_x, mouse_y, board):
    """
    Verifica si el mouse está sobre el área del tablero.

    :param mouse_x: Coordenada X del mouse.
    :param mouse_y: Coordenada Y del mouse.
    :param board: Objeto del tablero.
    :return: True si el mouse está sobre el tablero, False de lo contrario.
    """
    board_width = board.cell_size * board.board_size
    board_height = board.cell_size * board.board_size
    return (
        board.start_x <= mouse_x <= board.start_x + board_width and
        board.start_y <= mouse_y <= board.start_y + board_height
    )
