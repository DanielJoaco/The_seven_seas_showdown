import pygame
from modules.config import config
from modules.utils import draw_panel, draw_attack_board

class UI:
    def __init__(self):
        self.screen = None
        self.clock = pygame.time.Clock()

    def init_screen(self):
        """Inicializa la pantalla de Pygame según la configuración en config."""
        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("The Seven Seas Showdown")

    def fill_background(self):
        """Rellena la pantalla con el color de fondo actual de config."""
        self.screen.fill(config.colors["background"])

    def update_display(self):
        """Actualiza la pantalla y controla el framerate."""
        pygame.display.flip()
        self.clock.tick(60)

    def draw_game_state(self, screen, player, bot, player_board, bot_board, current_turn, current_round):
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
            "player_turn_attack": f"{player.name}, selecciona un ataque",
            "attack_selection": f"{player.name}, atacando a {bot.name}",
        }[current_turn]
        title_text = font_title.render(title, True, config.colors["text"])
        title_rect = title_text.get_rect(center=(config.WINDOW_WIDTH // 2, 40))
        screen.blit(title_text, title_rect)

        # Paneles de información
        draw_panel(screen, 20, 80, 300, 140, {"Jugador": player.name, "Vida": player.life, "Estamina": player.stamina}, font_info)
        draw_panel(screen, config.WINDOW_WIDTH - 320, 80, 300, 140, {"Bot": bot.name, "Vida": bot.life, "Estamina": bot.stamina}, font_info)

        # Dibujar el tablero del jugador
        if player_board:
            player_board.start_x = 50  # Posición a la izquierda
            player_board.start_y = 260
            player_board.draw(screen)

        # Dibujar el tablero de ataque del jugador (su vista del tablero del bot)
        if bot_board:
            bot_board.start_x = config.WINDOW_WIDTH - bot_board.pixel_size - 50  # Posición a la derecha
            bot_board.start_y = 260
            draw_attack_board(screen, bot_board, player.attack_board)

ui = UI()
