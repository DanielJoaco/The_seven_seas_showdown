import pygame
from modules.config import config

class UI:
    def __init__(self):
        self.screen = None
        self.clock = pygame.time.Clock()
        self.fondo = None  # Aquí se almacenará la imagen de fondo

    def init_screen(self, backgraound_image="battle"):
        """Inicializa la pantalla de Pygame según la configuración en config."""
        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("The Seven Seas Showdown")
        
        # Cargar la imagen de fondo
        if backgraound_image == "menu":
            self.fondo = pygame.image.load("../assets/images/menu_1.png")
            font_title = pygame.font.Font(config.font_bold, 54)
            title = "The Seven Seas Showdown"
            title_text = font_title.render(title, True, config.colors["text"])
            title_rect = title_text.get_rect(center=(config.WINDOW_WIDTH // 2, 40))
            self.screen.blit(title_text, title_rect)
    
        elif backgraound_image == "battle":
            self.fondo = pygame.image.load("../assets/images/battle_1.png")
        # Asegurarse de que la imagen se ajusta al tamaño de la ventana
        self.fondo = pygame.transform.scale(self.fondo, (config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

    def fill_background(self):
        """Dibuja la imagen de fondo en la pantalla."""
        self.screen.blit(self.fondo, (0, 0))

    def update_display(self):
        """Actualiza la pantalla y controla el framerate."""
        pygame.display.flip()
        self.clock.tick(30)  # Puedes ajustar el framerate según tus necesidades

    def draw_game_state(self, screen, player, bot, player_board, bot_board, current_turn, current_round):
        """
        Dibuja el estado actual del juego con la información de los jugadores y tableros.
        """
        # Llamamos a fill_background para dibujar la imagen de fondo
        self.fill_background()

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
        self.draw_panel(screen, 20, 80, 300, 140, {"Jugador": player.name, "Vida": player.life, "Estamina": player.stamina}, font_info)
        self.draw_panel(screen, config.WINDOW_WIDTH - 320, 80, 300, 140, {"Bot": bot.name, "Vida": bot.life, "Estamina": bot.stamina}, font_info)

        # Dibujar el tablero del jugador
        if player_board:
            player_board.start_x = 50  # Posición a la izquierda
            player_board.start_y = 260
            player_board.draw(screen)

        # Dibujar el tablero de ataque del jugador (su vista del tablero del bot)
        if bot_board:
            bot_board.start_x = config.WINDOW_WIDTH - bot_board.pixel_size - 50  # Posición a la derecha
            bot_board.start_y = 260
            self.draw_attack_board(screen, bot_board, player.attack_board)

    def draw_panel(self, screen, x, y, width, height, info, font):
        """
        Dibuja un panel de información en la pantalla.
        """
        pygame.draw.rect(
            screen, config.colors["background"], (x, y, width, height), border_radius=10
        )
        pygame.draw.rect(
            screen, config.colors["border"], (x, y, width, height), 2, border_radius=10
        )
        padding = 10
        line_height = 30
        for i, (key, value) in enumerate(info.items()):
            text = font.render(f"{key}: {value}", True, config.colors["text"])
            screen.blit(text, (x + padding, y + padding + i * line_height))
        
    def draw_attack_board(self, screen, board, attack_board, player="player"):
        """
        Dibuja el tablero de ataque del jugador (su vista del tablero del bot).
        """
        # Dibujar números de columnas (1 a N) en la parte superior
        font = pygame.font.Font(config.font_regular, 12)
        for col in range(board.board_size):
            number_text = font.render(str(col + 1), True, config.colors["text"])
            text_rect = number_text.get_rect(
                center=(board.start_x + col * board.cell_size + board.cell_size // 2, board.start_y - board.cell_size // 2)
            )
            screen.blit(number_text, text_rect)

        # Dibujar letras de filas (A, B, C, ...) en el lado derecho
        for row in range(board.board_size):
            letter_text = font.render(chr(65 + row), True, config.colors["text"])
            text_rect = letter_text.get_rect(
                center=(board.start_x + board.board_size * board.cell_size + board.cell_size // 2,
                        board.start_y + row * board.cell_size + board.cell_size // 2)
            )
            screen.blit(letter_text, text_rect)

        # Dibujar las celdas del tablero de ataque
        for row in range(board.board_size):
            for col in range(board.board_size):
                x = board.start_x + col * board.cell_size
                y = board.start_y + row * board.cell_size

                attack_cell = attack_board[row][col]
                state = attack_cell["state"]

                if state == 0:
                    color = config.colors["cell"]
                elif state == 1:
                    color = config.colors["water"]
                elif state == 2:
                    color = config.colors["hit"]
                elif state == 4:
                    color = config.colors["shielded"]
                else:
                    color = config.colors["cell"]

                pygame.draw.rect(screen, color, (x, y, board.cell_size, board.cell_size))
                pygame.draw.rect(screen, config.colors["border"], (x, y, board.cell_size, board.cell_size), 1)

ui = UI()
