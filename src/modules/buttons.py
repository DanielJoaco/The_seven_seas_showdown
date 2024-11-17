import pygame
from modules.config import config


def draw_button(screen, x, y, width, height, text, font, is_hovered=False):
    """
    Dibuja un botón en la pantalla.
    :param screen: Superficie donde se dibuja.
    :param x: Coordenada X del botón.
    :param y: Coordenada Y del botón.
    :param width: Ancho del botón.
    :param height: Alto del botón.
    :param text: Texto a mostrar en el botón.
    :param font: Fuente para el texto.
    :param is_hovered: Si el botón está siendo seleccionado o resaltado.
    """
    button_color = config.colors["selected_cell"] if is_hovered else config.colors["cell"]
    border_color = config.colors["selected_border"] if is_hovered else config.colors["border"]

    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, border_color, button_rect, width=2, border_radius=10)

    text_surface = font.render(text, True, config.colors["text"])
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)


def is_mouse_over_button(mouse_x, mouse_y, x, y, width, height):
    """
    Verifica si el mouse está sobre el botón.
    :param mouse_x: Coordenada X del mouse.
    :param mouse_y: Coordenada Y del mouse.
    :param x: Coordenada X del botón.
    :param y: Coordenada Y del botón.
    :param width: Ancho del botón.
    :param height: Alto del botón.
    :return: True si el mouse está sobre el botón, False en caso contrario.
    """
    return x <= mouse_x <= x + width and y <= mouse_y <= y + height


def handle_button_interaction(mouse_x, mouse_y, buttons):
    """
    Detecta cuál botón está siendo interactuado y devuelve su índice.
    :param mouse_x: Coordenada X del mouse.
    :param mouse_y: Coordenada Y del mouse.
    :param buttons: Lista de botones con su posición y dimensiones [(x, y, width, height), ...].
    :return: Índice del botón interactuado, o None si no hay interacción.
    """
    for index, (x, y, width, height) in enumerate(buttons):
        if is_mouse_over_button(mouse_x, mouse_y, x, y, width, height):
            return index
    return None
