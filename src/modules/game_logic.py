import pygame
import time
from modules.config import config
from modules.utils import (
    handle_navigation_and_selection,
    can_place_ship,
    place_ship_on_board,
    display_message,
    draw_preview,
    toggle_orientation,
)
from modules.dice import dice_turn, process_dice_roll
from modules.buttons import draw_action_buttons, is_mouse_over_button
from modules.ui import ui
import modules.attacks_logic as attacks_logic

def place_ships(screen, player_board, player_fleet, player, bot, bot_board):
    """
    Permite al jugador colocar barcos en su tablero.
    """
    current_ship_index = 0
    orientation = "H"
    selected_row, selected_col = 0, 0

    while current_ship_index < len(player_fleet):
        ship = player_fleet[current_ship_index]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            selected_row, selected_col, orientation, confirm = handle_navigation_and_selection(
                event,
                selected_row,
                selected_col,
                player_board.board_size,
                orientation,
                attack_type=None,
                board=player_board,
                screen=screen
            )

            if confirm:
                if can_place_ship(player_board.grid, ship.size, selected_row, selected_col, orientation):
                    place_ship_on_board(player_board, ship, selected_row, selected_col, orientation)
                    current_ship_index += 1
                    break
                else:
                    display_message(screen, "No se puede colocar el barco aquí.")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    orientation = toggle_orientation(orientation)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                orientation = toggle_orientation(orientation)

        screen.fill(config.colors["background"])
        ui.draw_game_state(screen, player, bot, player_board, bot_board, "placing_player_ships", 0)
        draw_central_area(
            screen,
            "placing_player_ships",
            player=player,
            bot_board=None,
            selected_row=selected_row,
            selected_col=selected_col,
            message=f"{player.name}, coloca tu {ship.name}",
        )
        draw_preview(screen, player_board, selected_row, selected_col, orientation, size=ship.size)
        pygame.display.flip()

    return True

def draw_central_area(
    screen,
    current_turn,
    player=None,
    bot=None,
    bot_board=None,
    selected_row=None,
    selected_col=None,
    message=None,
    current_round=1
):
    """
    Maneja la lógica del área central del turno, renderizando los botones y el mensaje.
    """
    button_area_width = 400
    button_area_height = 150
    button_area_x = config.WINDOW_WIDTH // 2 - button_area_width // 2
    button_area_y = config.WINDOW_HEIGHT // 2 - button_area_height // 2
    button_area_rect = pygame.Rect(
        button_area_x, button_area_y, button_area_width, button_area_height
    )

    pygame.draw.rect(
        screen, config.colors["background"], button_area_rect, border_radius=10
    )

    if current_turn == "player_turn" and player:
        dice_result = dice_turn(screen, "Tu turno: tira el dado", button_area_rect)
        message = process_dice_roll(dice_result, player)
        current_turn = "player_turn_attack"

    elif current_turn == "player_turn_attack":
        if player.turn_skipped:
            display_message(screen, "Perdiste tu turno.")
            time.sleep(2)
            player.turn_skipped = False
            return "bot_turn"
        else:
            action = draw_action_buttons(screen, button_area_rect, player)
            ui.update_display()

            if action:
                current_turn = attacks_logic.handle_attack_action(
                    screen, player, bot, bot_board, action, current_round
                )

    if message:
        font = pygame.font.Font(config.font_regular, 24)
        message_text = font.render(message, True, config.colors["text"])
        message_text_rect = message_text.get_rect(
            center=(button_area_rect.centerx, button_area_rect.centery)
        )
        screen.blit(message_text, message_text_rect)

    return current_turn
