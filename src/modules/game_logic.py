import pygame
import random
import time
from .config import config
from .ui import ui
from .utils import handle_keyboard_navigation, handle_mouse_selection

def place_ships(player, board):
    """
    Lógica de colocación interactiva de barcos para el jugador.
    """
    orientation = "H"
    selected_row, selected_col = 0, 0
    current_ship_index = 0
    current_ship_count = 0
    fleet = player.fleet

    while current_ship_index < len(fleet):
        ship = fleet[current_ship_index]

        # Verificar si la cantidad del tipo de barco actual ya fue colocada
        if current_ship_count >= ship.quantity:
            current_ship_index += 1
            current_ship_count = 0
            continue

        # Ajustar coordenadas de selección para mantener el barco dentro de los límites
        if orientation == "H":
            selected_col = min(selected_col, board.board_size - ship.size)
            selected_row = min(selected_row, board.board_size - 1)
        else:
            selected_row = min(selected_row, board.board_size - ship.size)
            selected_col = min(selected_col, board.board_size - 1)

        # Dibujar el tablero y resaltar la ubicación potencial del barco
        ui.fill_background()
        board.draw(ui.screen)

        # Verificar si el barco cabe en la posición seleccionada
        if player.can_place_ship(ship, selected_row, selected_col, orientation):
            for i in range(ship.size):
                r = selected_row + (i if orientation == "V" else 0)
                c = selected_col + (i if orientation == "H" else 0)
                pygame.draw.rect(
                    ui.screen,
                    config.selected_cell_color,
                    pygame.Rect(board.start_x + c * board.cell_size, board.start_y + r * board.cell_size, board.cell_size, board.cell_size)
                )

        ui.update_display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    orientation = "V" if orientation == "H" else "H"
                elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    selected_row, selected_col = handle_keyboard_navigation(event, selected_row, selected_col, board.board_size, board.board_size)
                elif event.key == pygame.K_RETURN:
                    if player.place_ship(ship, selected_row, selected_col, orientation):
                        current_ship_count += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player.place_ship(ship, selected_row, selected_col, orientation):
                        current_ship_count += 1
                elif event.button == 3:
                    orientation = "V" if orientation == "H" else "H"

            # Actualizar la posición seleccionada según el ratón solo si hay un evento de movimiento o clic del ratón
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                selected_cell = handle_mouse_selection(event, board.start_x, board.start_y, board.cell_size, board.board_size)
                if selected_cell:
                    selected_row, selected_col = selected_cell

def start_battle(player, bot):
    """
    Inicia la fase de combate entre el jugador y el bot en una interfaz gráfica.
    Cada turno incluye un ataque de jugador y un ataque de bot, alternando hasta que haya un ganador.
    """
    turn_count = 1
    game_over = False
    selected_row, selected_col = 0, 0

    while not game_over:
        print(f"\nInicio del Turno {turn_count}")

        # Turno del Jugador
        player_turn_result = False
        while not player_turn_result:
            ui.fill_background()
            player.board.draw(ui.screen)
            draw_attack_board(ui.screen, bot.board, selected_row, selected_col)
            display_turn_counter(turn_count)
            ui.update_display()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    selected_row, selected_col = handle_keyboard_navigation(event, selected_row, selected_col, bot.board.board_size, bot.board.board_size)
                    if event.key == pygame.K_RETURN:
                        result = attempt_attack(player, bot, selected_row, selected_col)
                        if result in ["hit", "miss"]:
                            player_turn_result = True
                            pygame.time.delay(2000)  # Espera de 2 segundos después del ataque del jugador
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    selected_cell = handle_mouse_selection(event, bot.board.start_x, bot.board.start_y, bot.board.cell_size, bot.board.board_size)
                    if selected_cell:
                        selected_row, selected_col = selected_cell
                        if event.button == 1:
                            result = attempt_attack(player, bot, selected_row, selected_col)
                            if result in ["hit", "miss"]:
                                player_turn_result = True
                                pygame.time.delay(2000)  # Espera de 2 segundos después del ataque del jugador

                # Verificar condición de victoria después del ataque del jugador
                if bot.life <= 0:
                    game_over = True
                    print(f"{player.name} ha ganado el juego en {turn_count} turnos!")
                    display_winner(ui.screen, player.name, turn_count)
                    return  # Salir del juego si el jugador gana

        # Turno del Bot (con retardo para visualización)
        print(f"Turno del Bot en proceso... (mostrando ataque por 5 segundos)")
        display_bot_attack(bot, player)

        # Verificar condición de victoria después del ataque del bot
        if player.life <= 0:
            game_over = True
            print(f"{bot.name} ha ganado el juego en {turn_count} turnos!")
            display_winner(ui.screen, bot.name, turn_count)
            return  # Salir del juego si el bot gana

        turn_count += 1

def attempt_attack(player, opponent, row, col):
    """
    Ejecuta un ataque en la posición (row, col) del tablero del oponente y devuelve el resultado.
    """
    result = opponent.receive_attack(row, col)
    if result == "hit":
        print(f"{player.name} acertó en ({row}, {col})!")
    elif result == "miss":
        print(f"{player.name} falló en ({row}, {col}).")
    else:
        print(f"({row}, {col}) ya fue atacado.")
    return result

def display_bot_attack(bot, player):
    """
    Muestra el tablero de ataque del bot durante 5 segundos, realizando el ataque en el segundo 3.
    """
    attack_row = random.randint(0, player.board.board_size - 1)
    attack_col = random.randint(0, player.board.board_size - 1)

    for i in range(5):
        ui.fill_background()
        draw_attack_board(ui.screen, player.board, None, None)

        font = pygame.font.SysFont(None, 36)
        attack_text = font.render(f"Ataque del bot en {5 - i} segundos", True, config.text_color)
        ui.screen.blit(attack_text, (10, 50))

        if i == 3:
            result = attempt_attack(bot, player, attack_row, attack_col)
            print(f"Bot atacó en ({attack_row}, {attack_col}) con resultado: {result}")

        ui.update_display()
        pygame.time.delay(1000)

def draw_attack_board(screen, board, selected_row=None, selected_col=None):
    """
    Dibuja el tablero de ataque del oponente, mostrando las celdas atacadas y el estado actual.
    Resalta la celda seleccionada con un borde.
    """
    for row in range(board.board_size):
        for col in range(board.board_size):
            x = board.start_x + col * board.cell_size
            y = board.start_y + row * board.cell_size
            cell = board.grid[row][col]

            if cell["state"] == 0:
                color = config.cell_color
            elif cell["state"] == 2:
                color = (105, 105, 105)
            elif cell["state"] == 3:
                color = (255, 0, 0)
            else:
                color = config.cell_color

            pygame.draw.rect(screen, color, pygame.Rect(x, y, board.cell_size, board.cell_size))
            pygame.draw.rect(screen, config.border_color, pygame.Rect(x, y, board.cell_size, board.cell_size), width=config.BORDER_WIDTH)

    if selected_row is not None and selected_col is not None:
        highlight_x = board.start_x + selected_col * board.cell_size
        highlight_y = board.start_y + selected_row * board.cell_size
        pygame.draw.rect(screen, config.selected_border_color, pygame.Rect(highlight_x, highlight_y, board.cell_size, board.cell_size), width=3)

def display_turn_counter(turn_count):
    """
    Muestra el contador de turnos en pantalla.
    """
    font = pygame.font.SysFont(None, 36)
    turn_text = font.render(f"Turno: {turn_count}", True, config.text_color)
    ui.screen.blit(turn_text, (10, 10))

def display_winner(screen, winner_name, turn_count):
    """
    Muestra el mensaje de victoria en la pantalla y pausa el juego para que el jugador pueda verlo.
    """
    font = pygame.font.SysFont(None, 48)
    winner_text = font.render(f"{winner_name} ha ganado en {turn_count} turnos!", True, config.text_color)
    text_rect = winner_text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2))
    screen.blit(winner_text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)  # Espera de 3 segundos antes de cerrar
