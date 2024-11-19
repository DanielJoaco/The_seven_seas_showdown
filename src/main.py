import pygame
from modules.config import config
from modules.board import Board
from modules.ui import ui
from modules.player import Player
from modules.buttons import draw_button, handle_button_interaction, is_mouse_over_button
from modules.game_logic import place_ships, draw_central_area
import time
from modules.utils import handle_menu_navigation  # Importar función de navegación de menú


def initialize_game():
    """Inicializa los elementos principales del juego: tableros y jugadores."""
    board = Board(15)
    player = Player("Jugador", board)
    bot_board = Board(15)
    bot = Player("Bot", bot_board)
    return board, player, bot_board, bot


def main_menu():
    """Despliega el menú principal y maneja la navegación entre opciones."""
    ui.init_screen()
    font = pygame.font.Font(config.font_bold, 30)

    # Definir los botones del menú
    button_specs = [
        (config.WINDOW_WIDTH // 2 - 110, 200, 280, 60, "Start Game"),
        (config.WINDOW_WIDTH // 2 - 110, 300, 280, 60, "Show Rules"),
        (config.WINDOW_WIDTH // 2 - 110, 400, 280, 60, "Show Settings"),
        (config.WINDOW_WIDTH // 2 - 110, 500, 280, 60, "Exit"),
    ]

    selected_index = 0  # Botón seleccionado por defecto
    last_input = "keyboard"  # Para rastrear la última fuente de entrada
    num_buttons = len(button_specs)

    while True:
        ui.fill_background()

        # Obtener posición del mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Dibujar los botones
        for i, (x, y, width, height, text) in enumerate(button_specs):
            is_hovered = is_mouse_over_button(mouse_x, mouse_y, x, y, width, height)
            draw_button(ui.screen, x, y, width, height, text, font, is_hovered or i == selected_index)

        ui.update_display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Manejo de navegación con teclado usando la función utilitaria
            selected_index, confirm = handle_menu_navigation(event, selected_index, num_buttons)
            if confirm:
                return button_specs[selected_index][4]  # Acción seleccionada

            # Manejo de interacción con mouse
            hovered_index = handle_button_interaction(mouse_x, mouse_y, [(x, y, w, h) for x, y, w, h, _ in button_specs])
            if hovered_index is not None:
                if last_input != "mouse" or hovered_index != selected_index:
                    selected_index = hovered_index
                    last_input = "mouse"

                # Detección de clic para seleccionar
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return button_specs[hovered_index][4]  # Acción seleccionada


def start_game(board, player, bot_board, bot):
    """Inicia el flujo principal del juego."""
    running = True
    current_turn = "placing_player_ships"  # Estado inicial del juego
    current_round = 1  # Ronda inicial

    while running:
        # Limpia la pantalla y dibuja el estado actual del juego
        ui.fill_background()
        ui.draw_game_state(ui.screen, player, bot, board, bot_board, current_turn, current_round)
        ui.update_display()

        # Flujo de colocación de barcos
        if current_turn == "placing_player_ships":
            if place_ships(ui.screen, board, player.fleet, player, bot, bot_board):
                # Cambiar al estado de colocación de barcos del bot
                current_turn = "placing_bot_ships"
                ui.fill_background()
                ui.draw_game_state(ui.screen, player, bot, board, bot_board, current_turn, current_round)
                ui.update_display()
                time.sleep(1)
                bot.place_fleet_randomly()
                current_turn = "player_turn"

        # Flujo del turno del jugador
        elif current_turn == "player_turn":
            current_turn = draw_central_area(
                ui.screen,
                current_turn,
                player=player,
                bot=bot,  # Pasar el objeto bot
                bot_board=bot_board,  # Tablero del bot, necesario para ataques
            )
            ui.update_display()

        # Flujo del ataque del jugador
        elif current_turn == "player_turn_attack":
            current_turn = draw_central_area(
                ui.screen,
                current_turn,
                player=player,
                bot=bot,  # Pasar el objeto bot
                bot_board=bot_board,  # Tablero del bot
            )

        # Flujo del turno del bot
        elif current_turn == "bot_turn":
            # Aquí iría la lógica del turno del bot (pendiente de implementación)
            time.sleep(1)  # Simula el tiempo de acción del bot
            current_turn = "player_turn"
            current_round += 1

        # Manejo de eventos globales
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


def show_rules():
    """Despliega las reglas del juego."""
    running = True
    while running:
        print("Reglas del juego: Presiona ESC para regresar al menú principal.")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Salir del bucle de reglas


def show_settings():
    """Muestra las configuraciones del juego."""
    running = True
    while running:
        print("Configuraciones del juego: Presiona ESC para regresar al menú principal.")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Salir del bucle de configuraciones


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    # Configurar el icono de la ventana
    pygame.display.set_icon(config.icon)

    # Inicializar tableros y jugadores
    board, player, bot_board, bot = initialize_game()

    while True:
        # Mostrar menú principal y capturar la acción seleccionada
        action = main_menu()

        if action == "Start Game":
            start_game(board, player, bot_board, bot)
        elif action == "Show Rules":
            show_rules()
        elif action == "Show Settings":
            show_settings()
        elif action == "Exit":
            pygame.quit()
            exit()
