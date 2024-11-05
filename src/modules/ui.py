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
        self.screen.fill(config.background_color)

    def render_menu(self, button_specs, font, button_width=220, button_height=50, border_radius=20):
        """Dibuja los botones del menú en la pantalla, resaltando solo el botón seleccionado o el que está bajo el cursor."""
        
        # Obtener la posición del cursor del mouse
        mouse_pos = pygame.mouse.get_pos()
        
        # Identificar el índice del botón sobre el cual está el cursor (si aplica)
        hovered_index = None
        for i, (x, y, _, _) in enumerate(button_specs):
            if x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height:
                hovered_index = i
                break  # Solo un botón puede estar bajo el cursor

        # Dibujar los botones, resaltando únicamente el botón seleccionado o el que está bajo el cursor
        for i, (x, y, text, selected) in enumerate(button_specs):
            # Determinar si este botón está "activo" (seleccionado por teclado o bajo el cursor)
            is_active = (i == hovered_index) or (selected and hovered_index is None)

            # Colores de botón y borde según el estado activo
            button_color = config.selected_cell_color if is_active else config.cell_color
            border_color = config.selected_border_color if is_active else config.border_color

            # Crear el rectángulo del botón con esquinas redondeadas
            button_rect = pygame.Rect(x, y, button_width, button_height)
            
            # Dibujar el borde redondeado
            pygame.draw.rect(self.screen, border_color, button_rect, width=4, border_radius=border_radius)

            # Dibujar el fondo del botón
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=border_radius)

            # Renderizar el texto y centrarlo en el botón
            text_surface = font.render(text, True, config.text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

    def update_display(self):
        """Actualiza la pantalla y controla el framerate."""
        pygame.display.flip()
        self.clock.tick(60)  # Controla el framerate a 60 FPS

# Crear una instancia global de UI
ui = UI()
