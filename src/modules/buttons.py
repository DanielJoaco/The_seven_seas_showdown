import pygame
from modules.config import config
from modules.ui import ui

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

def draw_action_buttons(screen, button_area_rect, player):
    """
    Genera y maneja la lógica de los botones de acción.
    """
    font = pygame.font.Font(config.font_regular, 20)

    # Configuración centralizada para botones
    button_config = {
        "width": 120,
        "height": 40,
        "horizontal_spacing": 20,
        "vertical_spacing": 10,
        "positions": [
            (button_area_rect.x + 20, button_area_rect.y + 20),
            (button_area_rect.x + 160, button_area_rect.y + 20),
            (button_area_rect.x + 20, button_area_rect.y + 70),
            (button_area_rect.x + 160, button_area_rect.y + 70),
            (button_area_rect.x + 90, button_area_rect.y + 120),
        ],
    }

    clock = pygame.time.Clock()

    # Botones de ataque y acciones
    buttons = [
        {"label": "A. Normal", "cost": 0, "action": "normal_attack"},
        {"label": "A. Lineal", "cost": 3, "action": "line_attack"},
        {"label": "A. Cuadrado", "cost": 4, "action": "square_attack"},
        {"label": "Radar", "cost": 4, "action": "use_radar"},
        {"label": "Escudo", "cost": 3, "action": "use_shield"},
    ]

    while True:  # Esperar hasta que el jugador seleccione un botón
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked_action = None  # Mantiene la acción seleccionada, si ocurre

        # Dibuja cada botón
        for button, (x, y) in zip(buttons, button_config["positions"]):
            is_hovered = is_mouse_over_button(
                mouse_x, mouse_y, x, y, button_config["width"], button_config["height"]
            )
            is_disabled = player.stamina < button["cost"]

            # Cambia el color según el estado
            color = (
                config.colors["disabled_button"]
                if is_disabled
                else config.colors["button"]
            )
            if is_hovered and not is_disabled:
                color = config.colors["hovered_button"]

            # Dibuja el botón
            pygame.draw.rect(
                screen,
                color,
                (x, y, button_config["width"], button_config["height"]),
                border_radius=10,
            )
            button_text = font.render(button["label"], True, config.colors["text"])
            button_text_rect = button_text.get_rect(
                center=(x + button_config["width"] // 2, y + button_config["height"] // 2)
            )
            screen.blit(button_text, button_text_rect)

        ui.update_display()

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button, (x, y) in zip(buttons, button_config["positions"]):
                    if is_mouse_over_button(
                        mouse_x, mouse_y, x, y, button_config["width"], button_config["height"]
                    ):
                        if player.stamina >= button["cost"]:  # Solo selecciona si tiene estamina suficiente
                            return button["action"]  # Retorna la acción seleccionada

        clock.tick(60)
