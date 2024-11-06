import pygame
import random
import time
from .config import config
from .ui import ui
from .utils import handle_keyboard_navigation, handle_mouse_selection

def place_ships(player, board):
    """Lógica de colocación interactiva de barcos para el jugador."""
    orientation = "H"  # Orientación inicial del barco
    selected_row, selected_col = 0, 0  # Posición inicial para la colocación de barcos
    current_ship_index = 0
    current_ship_count = 0  # Cuenta actual de barcos colocados del tipo actual
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
        else:  # Vertical
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
                # Cambiar orientación con 'V'
                if event.key == pygame.K_v:
                    orientation = "V" if orientation == "H" else "H"
                # Navegar con flechas, manteniéndose dentro del tablero
                elif event.key == pygame.K_UP:
                    selected_row = max(0, selected_row - 1)
                elif event.key == pygame.K_DOWN:
                    selected_row = min(board.board_size - 1, selected_row + 1)
                elif event.key == pygame.K_LEFT:
                    selected_col = max(0, selected_col - 1)
                elif event.key == pygame.K_RIGHT:
                    selected_col = min(board.board_size - 1, selected_col + 1)
                # Colocar barco con Enter
                elif event.key == pygame.K_RETURN:
                    if player.place_ship(ship, selected_row, selected_col, orientation):
                        current_ship_count += 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Cambiar orientación con clic izquierdo
                if event.button == 1:  # Clic izquierdo para colocar
                    if player.place_ship(ship, selected_row, selected_col, orientation):
                        current_ship_count += 1
                elif event.button == 3:  # Clic derecho para cambiar orientación
                    orientation = "V" if orientation == "H" else "H"

        # Actualizar la posición seleccionada según el mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        row = (mouse_y - board.start_y) // board.cell_size
        col = (mouse_x - board.start_x) // board.cell_size

        # Mantener la posición del mouse dentro de los límites del tablero para el barco actual
        if orientation == "H":
            col = min(col, board.board_size - ship.size)
            row = min(row, board.board_size - 1)
        else:  # Vertical
            row = min(row, board.board_size - ship.size)
            col = min(col, board.board_size - 1)

        # Actualizar las posiciones seleccionadas solo si el mouse está dentro del tablero
        if 0 <= row < board.board_size and 0 <= col < board.board_size:
            selected_row, selected_col = row, col

def start_battle(player, bot):
    """
    Inicia la fase de combate entre el jugador y el bot en una interfaz gráfica.
    Cada turno permite ataques adicionales si hay un acierto; cambia de turno en caso de fallo.
    """
    turn_count = 1
    game_over = False
    selected_row, selected_col = 0, 0
    clock = pygame.time.Clock()
    current_player = player
    opponent = bot
    is_player_turn = True  # Comienza el turno con el jugador

    while not game_over:
        print(f"\nInicio del Turno {turn_count}")

        turn_active = True  # El turno continúa hasta que el jugador actual falle
        while turn_active and not game_over:
            ui.fill_background()

            # Dibujar tablero del jugador y tablero de ataque del oponente
            player.board.draw(ui.screen)
            draw_attack_board(ui.screen, bot.board if is_player_turn else player.board, selected_row, selected_col)
            display_turn_counter(turn_count)
            ui.update_display()

            if is_player_turn:
                # Captura de eventos para el ataque del jugador
                player_turn_result = False  # Indica si se hizo un ataque

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Movimiento con teclado
                    elif event.type == pygame.KEYDOWN:
                        selected_row, selected_col = handle_keyboard_navigation(
                            event, selected_row, selected_col, bot.board.board_size, bot.board.board_size
                        )
                        if event.key == pygame.K_RETURN:
                            result = attempt_attack(player, bot, selected_row, selected_col)
                            player_turn_result = True  # Ataque realizado
                            if result == "miss":
                                turn_active = False  # Cambia de turno en caso de fallo
                            elif result == "hit":
                                turn_active = True  # Mantiene el turno si hay un impacto

                    # Movimiento y ataque con ratón
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        selected_cell = handle_mouse_selection(event, bot.board.start_x, bot.board.start_y,
                                                               bot.board.cell_size, bot.board.board_size)
                        if selected_cell:
                            selected_row, selected_col = selected_cell
                            if event.button == 1:  # Clic izquierdo para atacar
                                result = attempt_attack(player, bot, selected_row, selected_col)
                                player_turn_result = True  # Ataque realizado
                                if result == "miss":
                                    turn_active = False  # Cambia de turno en caso de fallo
                                elif result == "hit":
                                    turn_active = True  # Mantiene el turno si hay un impacto

                # Verificar condición de victoria después del ataque del jugador
                if player_turn_result and bot.life <= 0:
                    game_over = True
                    print(f"{player.name} ha ganado el juego en {turn_count} turnos!")
                    display_winner(ui.screen, player.name, turn_count)
                    return  # Finaliza el juego si el jugador gana

                ui.update_display()
                clock.tick(30)  # Controlar el framerate

            else:
                # Turno del bot con retardo
                display_bot_attack(bot, player)  # Ejecuta y muestra el ataque del bot con retardo
                turn_active = False  # Finaliza el turno del bot después de un ataque

                # Verificar condición de victoria después del ataque del bot
                if player.life <= 0:
                    game_over = True
                    print(f"{bot.name} ha ganado el juego en {turn_count} turnos!")
                    display_winner(ui.screen, bot.name, turn_count)
                    return  # Finaliza el juego si el bot gana

            # Alternar turnos entre jugador y bot
            if not turn_active:
                is_player_turn = not is_player_turn  # Cambia de turno

        turn_count += 1  # Incrementar el contador de turnos completos
        pygame.time.delay(500)  # Pausa breve al final del turno para transición visual

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
        player.board.draw(ui.screen)  # Dibuja el tablero del jugador
        draw_attack_board(ui.screen, player.board, attack_row if i >= 3 else None, attack_col if i >= 3 else None)
        display_turn_counter("Turno del Bot")

        font = pygame.font.SysFont(None, 36)
        attack_text = font.render(f"Ataque del bot en {5 - i} segundos", True, config.text_color)
        ui.screen.blit(attack_text, (10, 50))

        # En el segundo 3, el bot realiza el ataque
        if i == 3:
            result = attempt_attack(bot, player, attack_row, attack_col)
            print(f"Bot atacó en ({attack_row}, {attack_col}) con resultado: {result}")

        ui.update_display()
        pygame.time.delay(1000)  # Espera de 1 segundo entre actualizaciones

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

    # Resalta la celda seleccionada, si está definida
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