import pygame
from modules.config import config
from modules.board import Board
from modules.ui import ui
from modules.player import Player
import modules.game_logic as game_logic
from modules.utils import handle_keyboard_navigation, handle_mouse_selection

pygame.init()
pygame.font.init()

board = Board()
player = Player("Jugador", board)
bot_board = Board()  # Tablero separado para el bot
bot = Player("Bot", bot_board)
orientation = "H"  # Orientación inicial del barco
selected_row, selected_col = 0, 0  # Posición inicial para la colocación de barcos

def main_menu():
    ui.init_screen()

    while True:
        action = select_option()
        if action == "Start Game":
            print("Inicia el juego")
            game_logic.place_ships(player, board)
            bot.place_fleet_randomly()
            print(f"Barcos de {player.name} y {bot.name} han sido colocados.")
            game_logic.start_battle(player, bot)
            # Llamar a la función para iniciar la batalla (comentar si aún no está implementada)
            # start_battle(player, bot)
        elif action == "Show Rules":
            print("Mostrar reglas y cómo se juega")
        elif action == "Show Settings":
            print("Mostrar configuraciones")


def select_option():
    button_specs = [
        (config.WINDOW_WIDTH // 2 - 110, 200, "Start Game", False),
        (config.WINDOW_WIDTH // 2 - 110, 300, "Show Rules", False),
        (config.WINDOW_WIDTH // 2 - 110, 400, "Show Settings", False)
    ]

    font = pygame.font.SysFont(None, 50)
    selected_index = 0
    button_specs[selected_index] = button_specs[selected_index][:3] + (True,)  # Set initial selection
    clock = pygame.time.Clock()

    while True:
        ui.fill_background()
        ui.render_menu(button_specs, font, 280, 60, 50)
        ui.update_display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # Manejo de navegación en el menú con teclado
            if event.type == pygame.KEYDOWN:
                selected_index, _ = handle_keyboard_navigation(event, selected_index, 0, len(button_specs), 1)
                if event.key == pygame.K_RETURN:
                    return button_specs[selected_index][2]
                
            # Manejo de selección en el menú con ratón
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, (x, y, text, _) in enumerate(button_specs):
                    if x <= mouse_pos[0] <= x + 220 and y <= mouse_pos[1] <= y + 50:
                        return text

        clock.tick(30)

if __name__ == '__main__':
    main_menu()
