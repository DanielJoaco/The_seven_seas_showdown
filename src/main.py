import pygame
import time
from modules.config import config
from modules.board import Board
from modules.ui import ui
from modules.player import Player
from modules.game_logic import place_ships, draw_central_area
from modules.utils import handle_menu_navigation, display_message
from modules.buttons import draw_button, handle_button_interaction, is_mouse_over_button
from modules.attacks_logic import bot_attack

def initialize_game():
    """Inicializa los elementos principales del juego: tableros y jugadores."""
    board_size = 14
    player_board = Board(board_size)
    player = Player("Jugador", player_board)
    bot_board = Board(board_size)
    bot = Player("Bot", bot_board)
    return player_board, player, bot_board, bot

def main_menu():
    """Despliega el menú principal y maneja la navegación entre opciones."""
    ui.init_screen()
    font = pygame.font.Font(config.font_bold, 30)
    
    # Carga el archivo MP3
    pygame.mixer.music.load("./assets/sounds/menu.mp3")
    # Reproduce el MP3 en bucle (-1 significa bucle infinito)
    pygame.mixer.music.play(loops=-1)

    # Definir los botones del menú
    button_specs = [
        (config.WINDOW_WIDTH // 2 - 110, 200, 280, 60, "Start Game"),
        (config.WINDOW_WIDTH // 2 - 110, 300, 280, 60, "Show Rules"),
        (config.WINDOW_WIDTH // 2 - 110, 400, 280, 60, "Show Settings"),
        (config.WINDOW_WIDTH // 2 - 110, 500, 280, 60, "Exit"),
    ]

    selected_index = 0
    last_input = "keyboard"
    num_buttons = len(button_specs)

    while True:
        ui.fill_background()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Dibujar los botones
        for i, (x, y, width, height, text) in enumerate(button_specs):
            is_hovered = is_mouse_over_button(mouse_x, mouse_y, x, y, width, height)
            is_selected = is_hovered or i == selected_index
            draw_button(ui.screen, x, y, width, height, text, font, is_selected)

        ui.update_display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            selected_index, confirm = handle_menu_navigation(event, selected_index, num_buttons)
            if confirm:
                pygame.mixer.music.stop()
                return button_specs[selected_index][4]

            hovered_index = handle_button_interaction(
                mouse_x, mouse_y, [(x, y, w, h) for x, y, w, h, _ in button_specs]
            )
            if hovered_index is not None:
                if last_input != "mouse" or hovered_index != selected_index:
                    selected_index = hovered_index
                    last_input = "mouse"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.stop()
                    return button_specs[hovered_index][4]

def start_game(player_board, player, bot_board, bot):
    """Inicia el flujo principal del juego."""
    running = True
    current_turn = "placing_player_ships"
    current_round = 1
    # Cargar la imagen de fondo
    fondo = pygame.image.load("./assets/images/background.png")
    
    pygame.mixer.music.load("./assets/sounds/battle.mp3")
    pygame.mixer.music.play(loops=-1)

    # Asegúrate de que la imagen se ajusta al tamaño de la ventana
    fondo = pygame.transform.scale(fondo, (config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

    while running:
        ui.fill_background()
        ui.draw_game_state(
            ui.screen, player, bot, player_board, bot_board, current_turn, current_round
        )
        ui.update_display()

        if current_turn == "placing_player_ships":
            if place_ships(ui.screen, player_board, player.fleet, player, bot, bot_board):
                current_turn = "placing_bot_ships"
                ui.fill_background()
                ui.draw_game_state(
                    ui.screen,
                    player,
                    bot,
                    player_board,
                    bot_board,
                    current_turn,
                    current_round,
                )
                display_message(ui.screen, "Calculando posiciones...")
                ui.update_display()
                time.sleep(3)
                bot.place_fleet_randomly()
                current_turn = "player_turn"

        elif current_turn in ["player_turn", "player_turn_attack"]:
            current_turn = draw_central_area(
                ui.screen,
                current_turn,
                player=player,
                bot=bot,
                bot_board=bot_board,
                current_round=current_round
            )
            ui.update_display()
            time.sleep(1.5)

            # Al final del turno del jugador, ajustar estamina
            if current_turn == "bot_turn":
                if player.last_attack_type == "normal_attack":
                    ui.update_display()
                    player.stamina += 2
                else:
                    player.stamina += 1
                    ui.update_display()

        elif current_turn == "bot_turn":
            # Lógica de ataque del bot
            current_turn = bot_attack(
                ui.screen, bot, player, player_board, current_round
            )
            ui.update_display()
            current_round += 1  # Incrementar la ronda

            # Al final del turno del bot, ajustar estamina
            if current_turn.startswith("player_turn"):
                if bot.last_attack_type == "normal_attack":
                    bot.stamina += 2
                else:
                    bot.stamina += 1

        # Verificar condiciones de victoria
        if player.life <= 0:
            display_winner("Bot")
            running = False
        elif bot.life <= 0:
            display_winner("Jugador")
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                running = False

def display_winner(winner_name):
    """Muestra la pantalla de victoria."""
    font = pygame.font.Font(config.font_bold, 48)
    message = f"¡{winner_name} ha ganado!"
    text_surface = font.render(message, True, config.colors["text"])
    text_rect = text_surface.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2))

    ui.fill_background()
    ui.screen.blit(text_surface, text_rect)
    ui.update_display()
    time.sleep(5)

def display_text_screen(text_lines):
    """Despliega una pantalla de texto simple."""
    running = True
    font = pygame.font.Font(config.font_regular, 24)
    while running:
        ui.fill_background()
        y_offset = 100
        for line in text_lines:
            text_surface = font.render(line, True, config.colors["text"])
            text_rect = text_surface.get_rect(center=(config.WINDOW_WIDTH // 2, y_offset))
            ui.screen.blit(text_surface, text_rect)
            y_offset += 40
        ui.update_display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

def show_rules():
    """Despliega las reglas del juego."""
    rules = [
        "Reglas del Juego:",
        "1. Hundir todos los barcos enemigos.",
        "2. Los jugadores se turnan para atacar.",
        "Presiona ESC para regresar al menú principal.",
    ]
    display_text_screen(rules)

def show_settings():
    """Muestra las configuraciones del juego."""
    settings = [
        "Configuraciones:",
        "1. Tamaño del tablero: 15x15",
        "2. Modo de juego: Clásico",
        "Presiona ESC para regresar al menú principal.",
    ]
    display_text_screen(settings)

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.display.set_icon(config.icon)

    while True:
        player_board, player, bot_board, bot = initialize_game()
        action = main_menu()

        if action == "Start Game":
            start_game(player_board, player, bot_board, bot)
        elif action == "Show Rules":
            show_rules()
        elif action == "Show Settings":
            show_settings()
        elif action == "Exit":
            pygame.quit()
            exit()
