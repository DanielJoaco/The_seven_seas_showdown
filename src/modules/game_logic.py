import pygame
import time
from modules.config import config
from modules.utils import (
    is_within_bounds,
    handle_navigation_and_selection,
    place_ship_on_board,
    can_place_ship,
    draw_panel,
    draw_empty_board,
)
from modules.dice import dice_turn, process_dice_roll
from modules.buttons  import draw_action_buttons, is_mouse_over_button, handle_button_interaction
from modules.ui import ui


def place_ships(screen, player_board, player_fleet, player, bot, bot_board):
    """
    Permite al jugador colocar barcos en su tablero.
    """
    current_ship_index = 0
    orientation = "H"
    selected_row, selected_col = 0, 0

    while current_ship_index < len(player_fleet):
        screen.fill(config.colors["background"])

        # Barco actual
        ship = player_fleet[current_ship_index]

        # Dibuja el estado del juego
        draw_game_state(screen, player, bot, player_board, bot_board, "placing_player_ships", 0)

        # Mensaje central
        draw_central_area(screen,  "", f"{player.name}, coloca tu {ship.name}")

        # Vista previa del barco
        draw_ship_preview(screen, player_board, ship.size, selected_row, selected_col, orientation)

        # Actualiza la pantalla
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Manejar navegación y selección
            selected_row, selected_col = handle_navigation_and_selection(
                event,
                selected_row,
                selected_col,
                player_board.board_size,
                player_board.cell_size,
                player_board.start_x,
                player_board.start_y,
            )

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo: colocar barco
                    if can_place_ship(player_board, ship.size, selected_row, selected_col, orientation):
                        place_ship_on_board(player_board, ship, selected_row, selected_col, orientation)
                        current_ship_index += 1
                        break
                elif event.button == 3:  # Clic derecho: cambiar orientación
                    orientation = "H" if orientation == "V" else "V"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:  # Rotación con teclado
                    orientation = "H" if orientation == "V" else "V"
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):  # Confirmar colocación con teclado
                    if can_place_ship(player_board, ship.size, selected_row, selected_col, orientation):
                        place_ship_on_board(player_board, ship, selected_row, selected_col, orientation)
                        current_ship_index += 1
                        break

    return True


def draw_ship_preview(screen, board, size, start_row, start_col, orientation):
    """
    Dibuja una vista previa del barco en la posición indicada.
    """
    valid = can_place_ship(board, size, start_row, start_col, orientation)
    color = config.colors["selected_cell"] if valid else (255, 0, 0)

    for i in range(size):
        row = start_row + (i if orientation == "V" else 0)
        col = start_col + (i if orientation == "H" else 0)
        if is_within_bounds(row, col, board.board_size):
            x = board.start_x + col * board.cell_size
            y = board.start_y + row * board.cell_size
            pygame.draw.rect(screen, color, (x, y, board.cell_size, board.cell_size), 0)
            pygame.draw.rect(screen, config.colors["selected_border"], (x, y, board.cell_size, board.cell_size), 2)


def draw_game_state(screen, player, bot, player_board, bot_board, current_turn, current_round):
    """
    Dibuja el estado actual del juego con la información de los jugadores y tableros.
    """
    font_title = pygame.font.Font(config.font_bold, 54)
    font_info = pygame.font.Font(config.font_regular, 32)

    # Título del estado del juego
    title = {
        "placing_player_ships": "Colocando barcos del jugador",
        "placing_bot_ships": "Colocando barcos del bot",
        "player_turn": "Turno del jugador",
        "bot_turn": "Turno del bot",
        "game_over": "Juego terminado",
        "player_turn_attack": "Jugador atacando",
    }[current_turn]
    title_text = font_title.render(title, True, config.colors["text"])
    title_rect = title_text.get_rect(center=(config.WINDOW_WIDTH // 2, 40))
    screen.blit(title_text, title_rect)

    # Paneles de información
    draw_panel(screen, 20, 80, 200, 140, {"Jugador": player.name, "Vida": player.life, "Estamina": player.stamina}, font_info)
    draw_panel(screen, config.WINDOW_WIDTH - 220, 80, 200, 140, {"Bot": bot.name, "Vida": bot.life, "Estamina": bot.stamina}, font_info)

    # Ronda actual
    round_text = font_info.render(f"Ronda: {current_round}", True, config.colors["text"])
    round_rect = round_text.get_rect(center=(config.WINDOW_WIDTH // 2, 130))
    screen.blit(round_text, round_rect)

    # Tableros
    player_board.start_x = 50
    player_board.start_y = config.WINDOW_HEIGHT // 2 - player_board.pixel_size // 2 + 100
    player_board.draw(screen)

    bot_board.start_x = config.WINDOW_WIDTH - bot_board.pixel_size - 50
    bot_board.start_y = config.WINDOW_HEIGHT // 2 - bot_board.pixel_size // 2 + 100
    draw_empty_board(screen, bot_board)


def draw_central_area(screen, current_turn, player=None, message=None):
    """
    Maneja la lógica del área central del turno, renderizando los botones y el mensaje.
    """
    button_area_width = 300
    button_area_height = 150
    button_area_x = config.WINDOW_WIDTH // 2 - button_area_width // 2
    button_area_y = config.WINDOW_HEIGHT // 2 - button_area_height // 2
    button_area_rect = pygame.Rect(button_area_x, button_area_y, button_area_width, button_area_height)

    # Dibujar el área central
    pygame.draw.rect(screen, config.colors["background"], button_area_rect, border_radius=10)

    if current_turn == "player_turn" and player:
        dice_result = dice_turn(screen, "Tu turno: tira el dado", button_area_rect)
        message = process_dice_roll(dice_result, player)
        current_turn = "player_turn_attack"  # Cambiar al estado de ataque

    elif current_turn == "player_turn_attack":
        if player.turn_skipped:
            # Mostrar mensaje "Perdiste el turno"
            font = pygame.font.Font(config.font_regular, 24)
            message = "Perdiste el turno"
            message_text = font.render(message, True, config.colors["text"])
            message_text_rect = message_text.get_rect(center=(button_area_rect.centerx, button_area_rect.centery - 30))
            screen.blit(message_text, message_text_rect)

            # Botón "Finalizar turno"
            button_x = button_area_rect.centerx - 70
            button_y = button_area_rect.centery + 10
            button_width = 140
            button_height = 50

            mouse_x, mouse_y = pygame.mouse.get_pos()
            is_hovered = is_mouse_over_button(mouse_x, mouse_y, button_x, button_y, button_width, button_height)

            button_color = config.colors["hovered_button"] if is_hovered else config.colors["button"]
            pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height), border_radius=10)

            button_font = pygame.font.Font(config.font_regular, 20)
            button_text = button_font.render("Finalizar turno", True, config.colors["text"])
            button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            screen.blit(button_text, button_text_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and is_hovered:
                    player.turn_skipped = False  # Resetear el estado del jugador
                    return "bot_turn"  # Cambiar el estado al turno del bot
        else:
            # Renderizar botones de acción            
            action = draw_action_buttons(screen, button_area_rect, player)
            ui.update_display()
            if action:
                print(f"Acción seleccionada: {action}")
                # Implementar lógica basada en `action`
                return "bot_turn"  # Cambiar al estado de realizar acción

    if message:
        font = pygame.font.Font(config.font_regular, 24)
        message_text = font.render(message, True, config.colors["text"])
        message_text_rect = message_text.get_rect(center=button_area_rect.center)
        screen.blit(message_text, message_text_rect)

    return current_turn  # Mantener el estado actual si no hay cambios

