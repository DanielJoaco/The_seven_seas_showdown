import pygame
from .config import config

class UI:
    def __init__(self):
        self.screen = None
        self.clock = pygame.time.Clock()

    def init_screen(self):
        """Inicializa la pantalla de Pygame según la configuración en config."""
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("The Seven Seas Showdown")

    def fill_background(self):
        """Rellena la pantalla con el color de fondo actual de config."""
        self.screen.fill(config.colors["background"])

    def render_menu(self, button_specs, font, button_width=220, button_height=50, border_radius=20):
        """
        Dibuja los botones del menú en la pantalla.
        Retorna el índice del botón que está bajo el cursor, o None si no hay ninguno.
        """
        mouse_pos = pygame.mouse.get_pos()
        hovered_index = None

        for i, (x, y, text, selected) in enumerate(button_specs):
            # Detectar si el mouse está sobre el botón
            is_hovered = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
            is_active = selected or is_hovered

            # Colores según el estado
            button_color = config.colors["selected_cell"] if is_active else config.colors["cell"]
            border_color = config.colors["selected_border"] if is_active else config.colors["border"]

            # Dibujar el botón
            button_rect = pygame.Rect(x, y, button_width, button_height)
            pygame.draw.rect(self.screen, border_color, button_rect, width=4, border_radius=border_radius)
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=border_radius)

            # Renderizar texto
            text_surface = font.render(text, True, config.colors["text"])
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

            # Si el mouse está sobre este botón, registrar su índice
            if is_hovered:
                hovered_index = i

        return hovered_index

    def update_display(self):
        """Actualiza la pantalla y controla el framerate."""
        pygame.display.flip()
        self.clock.tick(60)  # Controla el framerate a 60 FPS

# Instancia global de UI
ui = UI()
