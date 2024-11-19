# modules/attacks_logic.py

import pygame
from modules.config import config
from modules.utils import (
    is_within_bounds,
    display_message,
    draw_preview,
    handle_navigation_and_selection
)
from modules.ui import ui


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
    selected_row, selected_col, orientation, confirm = select_attack_cell(screen, bot_board, player, bot, attack_type="normal_attack")
    
    if not confirm:
        return "player_turn"

    # Verificar si la celda ya ha sido atacada
    if player.attack_board[selected_row][selected_col]["state"] != 0:
        display_message(screen, "Esta celda ya ha sido atacada.")
        return "player_turn"

    # Realizar el ataque
    result = bot.receive_attack(selected_row, selected_col)
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
    selected_row, selected_col, orientation, confirm = select_attack_line(screen, bot_board, player, bot)

    if not confirm:
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
            result = bot.receive_attack(row, col)
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
    selected_row, selected_col, orientation, confirm = select_attack_cell(screen, bot_board, player, bot, attack_type="square_attack")

    if not confirm:
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
            result = bot.receive_attack(row, col)
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


def select_attack_cell(screen, bot_board, player, bot, attack_type="normal_attack"):
    """
    Permite al jugador seleccionar una celda objetivo en el tablero del bot.
    Similar a la colocación de barcos.

    :param screen: Superficie de Pygame para dibujar.
    :param bot_board: Tablero del bot.
    :param player: Jugador que realiza el ataque.
    :param bot: Bot que recibe el ataque.
    :param attack_type: Tipo de ataque ("normal_attack", "square_attack").
    :return: (fila, columna, orientación, confirmación) seleccionadas o (None, None, None, False) si se cancela.
    """
    selected_row, selected_col = 0, 0
    orientation = "H"  # Predeterminado (solo relevante para ciertos ataques)
    clock = pygame.time.Clock()

    while True:
        screen.fill(config.colors["background"])
        ui.draw_game_state(screen, player, bot, None, bot_board, "attack_selection", 0)
        if attack_type == "normal_attack":
            draw_preview(screen, bot_board, selected_row, selected_col, 1, orientation, preview_type="attack_normal")
        elif attack_type == "square_attack":
            draw_preview(screen, bot_board, selected_row, selected_col, 2, orientation, preview_type="attack_square")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Manejar navegación y selección usando la función utilitaria
            selected_row, selected_col, orientation, confirm = handle_navigation_and_selection(
                event,
                selected_row,
                selected_col,
                bot_board.board_size,
                orientation,
                attack_type,
                bot_board,
                screen
            )

            if confirm:
                return selected_row, selected_col, orientation, True

        clock.tick(60)


def select_attack_line(screen, bot_board, player, bot):
    """
    Permite al jugador seleccionar una fila o columna para un ataque lineal.

    :param screen: Superficie de Pygame para dibujar.
    :param bot_board: Tablero del bot.
    :param player: Jugador que realiza el ataque.
    :param bot: Bot que recibe el ataque.
    :return: (fila, columna, orientación, confirmación) seleccionadas o (None, None, None, False) si se cancela.
    """
    selected_row, selected_col = 0, 0
    orientation = "H"  # Predeterminado
    clock = pygame.time.Clock()

    while True:
        screen.fill(config.colors["background"])
        ui.draw_game_state(screen, player, bot, None, bot_board, "attack_selection", 0)
        draw_preview(screen, bot_board, selected_row, selected_col, 
                    1, 
                    orientation, 
                    preview_type="attack_line")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Manejar navegación y selección usando la función utilitaria
            selected_row, selected_col, orientation, confirm = handle_navigation_and_selection(
                event,
                selected_row,
                selected_col,
                bot_board.board_size,
                orientation,
                "line_attack",
                bot_board,
                screen
            )

            if confirm:
                return selected_row, selected_col, orientation, True

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
