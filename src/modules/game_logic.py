import pygame
from modules.config import config
from modules.utils import is_within_bounds, handle_keyboard_navigation, handle_mouse_selection
from modules.dice import dice_turn

def place_ships(screen, player_board, player_fleet, player, bot, bot_board):
    """
    Permite al jugador colocar barcos en su tablero, actualizando visualmente el estado del juego.
    """
    current_ship_index = 0
    orientation = "H"  # Orientación inicial: horizontal
    selected_row, selected_col = 0, 0
    running = True

    while running and current_ship_index < len(player_fleet):
        screen.fill(config.colors["background"])

        # Barco actual
        ship = player_fleet[current_ship_index]

        # Dibuja el estado completo del juego
        draw_game_state(screen, player, bot, player_board, bot_board, "placing_player_ships", 0)

        # Mensaje central sobre el barco actual
        message = f"{player.name}, coloca tu {ship.name}"
        draw_central_area(screen, "", message)

        # Dibuja la vista previa del barco
        draw_ship_preview(screen, player_board, ship.size, selected_row, selected_col, orientation)

        # Actualiza la pantalla
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Navegación con teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                selected_row, selected_col = handle_keyboard_navigation(event, selected_row, selected_col, player_board.board_size, player_board.board_size)
                if event.key == pygame.K_v:  # Cambiar orientación
                    orientation = "H" if orientation == "V" else "V"
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):  # Confirmar colocación
                    if can_place_ship(player_board, ship.size, selected_row, selected_col, orientation):
                        place_ship(player_board, ship, selected_row, selected_col, orientation)
                        current_ship_index += 1

            # Navegación y selección con mouse
            elif event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]:
                mouse_position = handle_mouse_selection(event, player_board.start_x, player_board.start_y, player_board.cell_size, player_board.board_size)
                if mouse_position:
                    selected_row, selected_col = mouse_position
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic izquierdo
                        if can_place_ship(player_board, ship.size, selected_row, selected_col, orientation):
                            place_ship(player_board, ship, selected_row, selected_col, orientation)
                            current_ship_index += 1
                    elif event.button == 3:  # Clic derecho
                        orientation = "H" if orientation == "V" else "V"

    return current_ship_index == len(player_fleet)

def draw_panel(screen, x, y, width, height, info, font):
    """
    Dibuja un panel de información en la pantalla.
    :param screen: Superficie donde se dibujará.
    :param x: Coordenada X del panel.
    :param y: Coordenada Y del panel.
    :param width: Ancho del panel.
    :param height: Alto del panel.
    :param info: Diccionario con claves y valores a mostrar.
    :param font: Fuente para el texto.
    """
    pygame.draw.rect(screen, config.colors["background"], (x, y, width, height), border_radius=10)
    for i, (key, value) in enumerate(info.items()):
        text = font.render(f"{key}: {value}", True, config.colors["text"])
        screen.blit(text, (x + 10, y + 10 + i * 40))


def draw_game_state(screen, player, bot, player_board, bot_board, current_turn, current_round):
    """
    Dibuja el estado actual del juego con la información de los jugadores y tableros.
    """
    font_title = pygame.font.Font(config.font_bold, 54)
    font_info = pygame.font.Font(config.font_regular, 32)

    # Título del estado del juego
    game_state_title = {
        "placing_player_ships": "Colocando barcos del jugador",
        "placing_bot_ships": "Colocando barcos del bot",
        "player_turn": "Turno del jugador",
        "bot_turn": "Turno del bot",
        "game_over": "Juego terminado"
    }
    title_text = font_title.render(game_state_title.get(current_turn, "Estado desconocido"), True, config.colors["text"])
    title_rect = title_text.get_rect(center=(config.WINDOW_WIDTH // 2, 40))
    screen.blit(title_text, title_rect)

    # Información del jugador
    draw_panel(screen, 20, 80, 200, 140, {
        "Jugador": player.name,
        "Vida": player.life,
        "Estamina": player.stamina
    }, font_info)

    # Información del bot
    draw_panel(screen, config.WINDOW_WIDTH - 220, 80, 200, 140, {
        "Bot": bot.name,
        "Vida": bot.life,
        "Estamina": bot.stamina
    }, font_info)

    # Ronda actual
    round_text = font_info.render(f"Ronda: {current_round}", True, config.colors["text"])
    round_rect = round_text.get_rect(center=(config.WINDOW_WIDTH // 2, 130))
    screen.blit(round_text, round_rect)

    # Dibujar tableros
    player_board.start_x = 50
    player_board.start_y = config.WINDOW_HEIGHT // 2 - player_board.pixel_size // 2 + 100
    player_board.draw(screen)

    bot_board.start_x = config.WINDOW_WIDTH - bot_board.pixel_size - 50
    bot_board.start_y = config.WINDOW_HEIGHT // 2 - bot_board.pixel_size // 2 + 100
    draw_empty_board(screen, bot_board)

    # Mensaje central
    draw_central_area(screen, "")

def draw_central_area(screen, current_turn, message=None, process_dice_roll=None):
    """
    Dibuja el área central para mostrar mensajes o botones según el turno.
    """
    button_area_width = 300
    button_area_height = 150
    button_area_x = config.WINDOW_WIDTH // 2 - button_area_width // 2
    button_area_y = config.WINDOW_HEIGHT // 2 - button_area_height // 2
    button_area_rect = pygame.Rect((button_area_x, button_area_y, button_area_width, button_area_height))

    # Dibuja el área central
    pygame.draw.rect(screen, config.colors["background"], button_area_rect, border_radius=10)

    if current_turn == "player_turn" and process_dice_roll:
        # Llamar a `dice_turn` para manejar el lanzamiento del dado
        dice_turn(screen, "Tu turno: tira el dado", button_area_rect, process_dice_roll)
    elif message:
        # Mostrar un mensaje si no es el turno del dado
        font_button = pygame.font.Font(config.font_regular, 24)
        message_text = font_button.render(message, True, config.colors["text"])
        message_text_rect = message_text.get_rect(center=button_area_rect.center)
        screen.blit(message_text, message_text_rect)

def draw_empty_board(screen, board):
    """
    Dibuja un tablero vacío (sin barcos visibles).
    """
    for row in range(board.board_size):
        for col in range(board.board_size):
            x = board.start_x + col * board.cell_size
            y = board.start_y + row * board.cell_size
            pygame.draw.rect(screen, config.colors["cell"], (x, y, board.cell_size, board.cell_size), 0)
            pygame.draw.rect(screen, config.colors["border"], (x, y, board.cell_size, board.cell_size), 1)

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

def place_ship(board, ship, start_row, start_col, orientation):
    """
    Coloca un barco en el tablero.
    """
    for i in range(ship.size):
        row = start_row + (i if orientation == "V" else 0)
        col = start_col + (i if orientation == "H" else 0)
        board.grid[row][col]["state"] = 1
        board.grid[row][col]["ship"] = ship.name

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
