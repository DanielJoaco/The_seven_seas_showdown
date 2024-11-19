import pygame
from modules.config import config
from modules.utils import (
    is_within_bounds,
    display_message,
    draw_preview,
    handle_navigation_and_selection,
    draw_attack_board,
    toggle_orientation
)
from modules.ui import ui
import math
import random
import time

def handle_attack_action(screen, player, bot, bot_board, attack_type, current_round):
    """
    Maneja la lógica para los diferentes tipos de ataques.
    """
    attack_handlers = {
        "normal_attack": handle_normal_attack,
        "line_attack": handle_line_attack,
        "square_attack": handle_square_attack,
        "use_radar": handle_radar,
        "use_shield": handle_shield,
    }

    handler = attack_handlers.get(attack_type)
    if handler:
        return handler(screen, player, bot, bot_board, current_round)
    else:
        print(f"Tipo de ataque desconocido: {attack_type}")
        return "player_turn"

def handle_normal_attack(screen, player, bot, bot_board, current_round):
    """
    Maneja un ataque normal.
    """
    attack_cost = 0
    if player.stamina < attack_cost:
        display_message(screen, "No tienes suficiente estamina para un ataque normal.")
        return "player_turn"

    selected_row, selected_col, orientation, confirm = select_attack_cell(
        screen, bot_board, player, bot, attack_type="normal_attack", current_round=current_round)

    if not confirm:
        return "player_turn"

    if player.attack_board[selected_row][selected_col]["state"] in [1, 2, 3]:
        display_message(screen, "Esta celda ya ha sido atacada.")
        return "player_turn"

    # Reduce estamina
    player.stamina -= attack_cost

    result = bot.receive_attack(selected_row, selected_col)
    update_attack_board(player, selected_row, selected_col, result)

    ui.draw_game_state(screen, player, bot, player.board, bot_board, "player_turn_attack", current_round)
    ui.update_display()

    if result == "hit":
        display_message(screen, "¡Impacto!")
        return "player_turn_attack"
    else:
        display_message(screen, "Fallaste.")
        return "bot_turn"

def handle_line_attack(screen, player, bot, bot_board, current_round):
    """
    Maneja un ataque lineal de 3 celdas.
    """
    attack_cost = 3
    if player.stamina < attack_cost:
        display_message(screen, "No tienes suficiente estamina para un ataque lineal.")
        return "player_turn"

    selected_row, selected_col, orientation, confirm = select_attack_line(
        screen, bot_board, player, bot, attack_type="line_attack", current_round=current_round)

    if not confirm:
        return "player_turn"

    # Reduce estamina
    player.stamina -= attack_cost

    # Ataque a 3 celdas en línea centradas en la celda seleccionada
    cells_to_attack = []
    offsets = [-1, 0, 1]
    if orientation == "H":
        for offset in offsets:
            col = selected_col + offset
            if is_within_bounds(selected_row, col, bot_board.board_size):
                cells_to_attack.append((selected_row, col))
    else:
        for offset in offsets:
            row = selected_row + offset
            if is_within_bounds(row, selected_col, bot_board.board_size):
                cells_to_attack.append((row, selected_col))

    any_hit = False
    for row, col in cells_to_attack:
        if player.attack_board[row][col]["state"] in [0, 5]:  # Permitir atacar celdas detectadas por radar
            result = bot.receive_attack(row, col)
            update_attack_board(player, row, col, result)
            if result == "hit":
                any_hit = True
            elif result == "shielded":
                any_hit = True

    ui.draw_game_state(screen, player, bot, player.board, bot_board, "player_turn_attack", current_round)
    ui.update_display()

    if any_hit:
        display_message(screen, "¡Ataque lineal acertó!")
        return "player_turn_attack"
    else:
        display_message(screen, "Ataque lineal falló.")
        return "bot_turn"

def handle_square_attack(screen, player, bot, bot_board, current_round):
    """
    Maneja un ataque cuadrado.
    """
    attack_cost = 4
    if player.stamina < attack_cost:
        display_message(screen, "No tienes suficiente estamina para un ataque cuadrado.")
        return "player_turn"

    selected_row, selected_col, orientation, confirm = select_attack_cell(
        screen, bot_board, player, bot, attack_type="square_attack", current_round=current_round
    )

    if not confirm:
        return "player_turn"

    # Reduce estamina
    player.stamina -= attack_cost

    cells_to_attack = [
        (selected_row + i, selected_col + j)
        for i in range(2)
        for j in range(2)
        if is_within_bounds(selected_row + i, selected_col + j, bot_board.board_size)
    ]

    any_hit = False
    for row, col in cells_to_attack:
        if player.attack_board[row][col]["state"] in [0, 5]:  # Permitir atacar celdas detectadas por radar
            result = bot.receive_attack(row, col)
            update_attack_board(player, row, col, result)
            if result == "hit":
                any_hit = True
            elif result == "shielded":
                any_hit = True

    ui.draw_game_state(screen, player, bot, player.board, bot_board, "player_turn_attack", current_round)
    ui.update_display()

    if any_hit:
        display_message(screen, "¡Ataque cuadrado acertó!")
        return "player_turn_attack"
    else:
        display_message(screen, "Ataque cuadrado falló.")
        return "bot_turn"

def handle_radar(screen, player, bot, bot_board, current_round):
    """
    Maneja la habilidad del radar.
    """
    ability_cost = 4
    if player.stamina < ability_cost:
        display_message(screen, "No tienes suficiente estamina para usar el radar.")
        return "player_turn"

    selected_row, selected_col, orientation, confirm = select_attack_cell(
        screen, bot_board, player, bot, attack_type="radar", current_round=current_round)

    if not confirm:
        return "player_turn"

    # Reduce estamina
    player.stamina -= ability_cost

    # Encontrar la celda más cercana con un barco enemigo no atacado
    nearest_cell = find_nearest_ship_cell(bot_board, selected_row, selected_col, player)
    if nearest_cell:
        row, col = nearest_cell
        player.attack_board[row][col]["state"] = 5  # Nuevo estado para radar detectado
        player.attack_board[row][col]["color"] = config.colors["radar_detected"]
        display_message(screen, "¡Radar detectó un barco cercano!")
    else:
        display_message(screen, "No se detectaron barcos cercanos.")

    ui.draw_game_state(screen, player, bot, player.board, bot_board, "player_turn_attack", current_round)
    ui.update_display()

    return "bot_turn"

def handle_shield(screen, player, bot, bot_board, current_round):
    """
    Maneja la habilidad del escudo.
    """
    ability_cost = 3
    if player.stamina < ability_cost:
        display_message(screen, "No tienes suficiente estamina para usar el escudo.")
        return "player_turn"

    # Reduce estamina
    player.stamina -= ability_cost

    # Activar el escudo temporal
    player.temp_shield = True
    display_message(screen, "¡Escudo activado! Estás protegido del próximo ataque.")

    # Permite atacar en el mismo turno
    return "player_turn_attack"

def select_attack_cell(screen, bot_board, player, bot, attack_type="normal_attack", current_round=1):
    """
    Permite al jugador seleccionar una celda objetivo en el tablero del bot.
    """
    selected_row, selected_col = 0, 0
    clock = pygame.time.Clock()

    running = True
    orientation = None
    while running:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Actualizar selección basada en la entrada
            selected_row, selected_col, orientation, confirm = handle_navigation_and_selection(
                event,
                selected_row,
                selected_col,
                bot_board.board_size,
                None,  # La orientación no es relevante para estos ataques
                attack_type,
                bot_board,
                screen
            )

            if confirm:
                return selected_row, selected_col, orientation, True

        # Actualizar la pantalla después de manejar los eventos
        screen.fill(config.colors["background"])
        ui.draw_game_state(screen, player, bot, player.board, bot_board, "attack_selection", current_round)

        # Dibujar el tablero de ataque
        draw_attack_board(screen, bot_board, player.attack_board)

        # Dibujar la previsualización de ataque
        draw_preview(
            screen,
            bot_board,
            selected_row,
            selected_col,
            orientation=None,  # No es necesario para estos ataques
            preview_type=attack_type,
            attack_board=player.attack_board
        )

        pygame.display.flip()
        clock.tick(60)

def select_attack_line(screen, bot_board, player, bot, attack_type="line_attack", current_round=1):
    """
    Permite al jugador seleccionar una línea de 3 celdas para un ataque lineal.
    Permite rotar la orientación con la tecla 'v' o clic derecho.
    """
    selected_row, selected_col = 0, 0
    orientation = "H"  # 'H' para Horizontal, 'V' para Vertical
    clock = pygame.time.Clock()

    running = True
    while running:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Actualizar selección basada en la entrada
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

            # Manejar rotación con tecla 'v'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    orientation = toggle_orientation(orientation)

            # Manejar rotación con clic derecho del ratón
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Clic derecho
                orientation = toggle_orientation(orientation)

            if confirm:
                return selected_row, selected_col, orientation, True

        # Actualizar la pantalla después de manejar los eventos
        screen.fill(config.colors["background"])
        ui.draw_game_state(screen, player, bot, player.board, bot_board, "attack_selection", current_round)

        # Dibujar el tablero de ataque
        draw_attack_board(screen, bot_board, player.attack_board)

        # Dibujar la previsualización de ataque
        draw_preview(
            screen,
            bot_board,
            selected_row,
            selected_col,
            orientation,
            preview_type=attack_type,
            attack_board=player.attack_board
        )

        pygame.display.flip()
        clock.tick(60)

def update_attack_board(player, row, col, result):
    """
    Actualiza el tablero de ataque del jugador basado en el resultado del ataque.
    """
    if result == "hit":
        player.attack_board[row][col]["state"] = 2  # Impacto
        player.attack_board[row][col]["color"] = config.colors["hit"]
    elif result == "miss":
        player.attack_board[row][col]["state"] = 1  # Agua
        player.attack_board[row][col]["color"] = config.colors["water"]
    elif result == "shielded":
        player.attack_board[row][col]["state"] = 4  # Escudo
        player.attack_board[row][col]["color"] = config.colors["shielded"]

def find_nearest_ship_cell(bot_board, selected_row, selected_col, player):
    """
    Encuentra la celda más cercana con un barco enemigo no atacado.
    """
    min_distance = math.inf
    nearest_cell = None
    for row in range(bot_board.board_size):
        for col in range(bot_board.board_size):
            cell = bot_board.grid[row][col]
            if cell["ship"] is not None and cell["state"] == 1:  # Barco no atacado
                distance = math.sqrt((row - selected_row) ** 2 + (col - selected_col) ** 2)
                if distance < min_distance:
                    # Verificar si la celda no ha sido detectada ya por el radar
                    if player.attack_board[row][col]["state"] != 5:
                        min_distance = distance
                        nearest_cell = (row, col)
    return nearest_cell

def bot_attack(screen, bot, player, player_board, current_round):
    """
    Lógica de ataque del bot.
    """
    time.sleep(1)
    abilities = ["normal_attack", "line_attack", "square_attack", "use_radar", "use_shield"]
    ability_costs = {
        "normal_attack": 0,
        "line_attack": 3,
        "square_attack": 4,
        "use_radar": 4,
        "use_shield": 3,
    }

    # Decidir qué habilidad usar
    if bot.stamina < 4:
        attack_type = "normal_attack"
    else:
        attack_type = random.choice(abilities)

    # Verificar si el bot tiene suficiente estamina
    if bot.stamina < ability_costs[attack_type]:
        attack_type = "normal_attack"

    # Narrar la acción del bot
    action_messages = {
        "normal_attack": "El bot realiza un ataque normal.",
        "line_attack": "El bot utiliza un ataque lineal.",
        "square_attack": "El bot utiliza un ataque cuadrado.",
        "use_radar": "El bot utiliza el radar.",
        "use_shield": "El bot activa un escudo.",
    }
    display_message(screen, action_messages[attack_type], delay=2000)

    # Ejecutar la acción
    bot_action_handlers = {
        "normal_attack": bot_handle_normal_attack,
        "line_attack": bot_handle_line_attack,
        "square_attack": bot_handle_square_attack,
        "use_radar": bot_handle_radar,
        "use_shield": bot_handle_shield,
    }

    handler = bot_action_handlers.get(attack_type)
    if handler:
        result = handler(screen, bot, player, player_board, current_round)
        ui.update_display()
        time.sleep(1)
        return result
    else:
        print(f"Tipo de ataque desconocido: {attack_type}")
        return "player_turn"

def bot_handle_normal_attack(screen, bot, player, player_board, current_round):
    """
    Maneja un ataque normal del bot.
    """
    attack_cost = 0
    bot.stamina -= attack_cost

    # Seleccionar aleatoriamente una celda no atacada
    valid_cells = [
        (row, col)
        for row in range(player_board.board_size)
        for col in range(player_board.board_size)
        if bot.attack_board[row][col]["state"] == 0
    ]
    if not valid_cells:
        return "player_turn"

    selected_row, selected_col = random.choice(valid_cells)

    result = player.receive_attack(selected_row, selected_col)
    update_bot_attack_board(bot, selected_row, selected_col, result)

    ui.draw_game_state(screen, player, bot, player_board, bot.board, "bot_turn", current_round)
    ui.update_display()

    if result == "hit":
        display_message(screen, "¡El bot te ha golpeado!", delay=1500)
    elif result == "shielded":
        display_message(screen, "¡Tu escudo bloqueó el ataque del bot!", delay=1500)
    else:
        display_message(screen, "El bot falló su ataque.", delay=1500)

    return "player_turn"

def bot_handle_line_attack(screen, bot, player, player_board, current_round):
    """
    Maneja un ataque lineal del bot.
    """
    attack_cost = 3
    bot.stamina -= attack_cost

    # Seleccionar orientación y celda aleatoriamente
    orientation = random.choice(["H", "V"])
    selected_row = random.randint(0, player_board.board_size - 1)
    selected_col = random.randint(0, player_board.board_size - 1)

    # Ataque a 3 celdas en línea centradas en la celda seleccionada
    cells_to_attack = []
    offsets = [-1, 0, 1]
    if orientation == "H":
        for offset in offsets:
            col = selected_col + offset
            if is_within_bounds(selected_row, col, player_board.board_size):
                cells_to_attack.append((selected_row, col))
    else:
        for offset in offsets:
            row = selected_row + offset
            if is_within_bounds(row, selected_col, player_board.board_size):
                cells_to_attack.append((row, selected_col))

    any_hit = False
    for row, col in cells_to_attack:
        if bot.attack_board[row][col]["state"] in [0, 5]:
            result = player.receive_attack(row, col)
            update_bot_attack_board(bot, row, col, result)
            if result == "hit":
                any_hit = True
            elif result == "shielded":
                any_hit = True

    ui.draw_game_state(screen, player, bot, player_board, bot.board, "bot_turn", current_round)
    ui.update_display()

    if any_hit:
        display_message(screen, "¡El bot acertó con su ataque lineal!", delay=1500)
    else:
        display_message(screen, "El bot falló su ataque lineal.", delay=1500)

    return "player_turn"

def bot_handle_square_attack(screen, bot, player, player_board, current_round):
    """
    Maneja un ataque cuadrado del bot.
    """
    attack_cost = 4
    bot.stamina -= attack_cost

    # Seleccionar aleatoriamente una celda
    selected_row = random.randint(0, player_board.board_size - 2)
    selected_col = random.randint(0, player_board.board_size - 2)

    cells_to_attack = [
        (selected_row + i, selected_col + j)
        for i in range(2)
        for j in range(2)
        if is_within_bounds(selected_row + i, selected_col + j, player_board.board_size)
    ]

    any_hit = False
    for row, col in cells_to_attack:
        if bot.attack_board[row][col]["state"] in [0, 5]:
            result = player.receive_attack(row, col)
            update_bot_attack_board(bot, row, col, result)
            if result == "hit":
                any_hit = True
            elif result == "shielded":
                any_hit = True

    ui.draw_game_state(screen, player, bot, player_board, bot.board, "bot_turn", current_round)
    ui.update_display()

    if any_hit:
        display_message(screen, "¡El bot acertó con su ataque cuadrado!", delay=1500)
    else:
        display_message(screen, "El bot falló su ataque cuadrado.", delay=1500)

    return "player_turn"

def bot_handle_radar(screen, bot, player, player_board, current_round):
    """
    Maneja la habilidad del radar del bot.
    """
    ability_cost = 4
    bot.stamina -= ability_cost

    # Seleccionar aleatoriamente una celda
    selected_row = random.randint(0, player_board.board_size - 1)
    selected_col = random.randint(0, player_board.board_size - 1)

    # Encontrar la celda más cercana con un barco enemigo no atacado
    nearest_cell = find_nearest_ship_cell(player_board, selected_row, selected_col, bot)
    if nearest_cell:
        row, col = nearest_cell
        bot.attack_board[row][col]["state"] = 5  # Estado especial para radar detectado
        bot.attack_board[row][col]["color"] = config.colors["radar_detected"]
        display_message(screen, "El bot usó el radar y encontró un barco.", delay=1500)
    else:
        display_message(screen, "El bot usó el radar pero no encontró nada.", delay=1500)

    return "player_turn"

def bot_handle_shield(screen, bot, player, player_board, current_round):
    """
    Maneja la habilidad del escudo del bot.
    """
    ability_cost = 3
    bot.stamina -= ability_cost

    # Activar el escudo temporal
    bot.temp_shield = True
    display_message(screen, "El bot ha activado un escudo.", delay=1500)

    return "player_turn"

def update_bot_attack_board(bot, row, col, result):
    """
    Actualiza el tablero de ataque del bot basado en el resultado del ataque.
    """
    if result == "hit":
        bot.attack_board[row][col]["state"] = 2  # Impacto
        bot.attack_board[row][col]["color"] = config.colors["hit"]
    elif result == "miss":
        bot.attack_board[row][col]["state"] = 1  # Agua
        bot.attack_board[row][col]["color"] = config.colors["water"]
    elif result == "shielded":
        bot.attack_board[row][col]["state"] = 4  # Escudo
        bot.attack_board[row][col]["color"] = config.colors["shielded"]

def find_nearest_ship_cell(board, selected_row, selected_col, player):
    """
    Encuentra la celda más cercana con un barco enemigo no atacado.
    """
    min_distance = math.inf
    nearest_cell = None
    for row in range(board.board_size):
        for col in range(board.board_size):
            cell = board.grid[row][col]
            if cell["ship"] is not None and cell["state"] == 1:  # Barco no atacado
                distance = math.sqrt((row - selected_row) ** 2 + (col - selected_col) ** 2)
                if distance < min_distance:
                    # Verificar si la celda no ha sido detectada ya por el radar
                    if player.attack_board[row][col]["state"] != 5:
                        min_distance = distance
                        nearest_cell = (row, col)
    return nearest_cell