import pygame
from modules.config import config

def draw_button(screen, x, y, width, height, text, font, is_hovered=False):
    """
    Dibuja un botón en la pantalla.
    """
    button_color = (
        config.colors["hovered_button"] if is_hovered else config.colors["button"]
    )
    border_color = (
        config.colors["selected_border"] if is_hovered else config.colors["border"]
    )

    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, border_color, button_rect, width=2, border_radius=10)

    text_surface = font.render(text, True, config.colors["text"])
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def is_mouse_over_button(mouse_x, mouse_y, x, y, width, height):
    """
    Verifica si el mouse está sobre el botón.
    """
    return x <= mouse_x <= x + width and y <= mouse_y <= y + height

def handle_button_interaction(mouse_x, mouse_y, buttons):
    """
    Detecta cuál botón está siendo interactuado y devuelve su índice.
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
        "positions": [
            (button_area_rect.x + 70, button_area_rect.y + 30),
            (button_area_rect.x + 210, button_area_rect.y + 30),
            (button_area_rect.x + 70, button_area_rect.y + 80),
            (button_area_rect.x + 210, button_area_rect.y + 80)
        ],
    }

    # Botones de ataque y acciones
    buttons = [
        {"label": "A. normal", "cost": 0, "action": "normal_attack"},
        {"label": "A. Lineal", "cost": 3, "action": "line_attack"},
        {"label": "A. Cuadrado", "cost": 4, "action": "square_attack"},
        {"label": "Escudo", "cost": 3, "action": "use_shield"},
    ]

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for button, (x, y) in zip(buttons, button_config["positions"]):
            is_hovered = is_mouse_over_button(
                mouse_x, mouse_y, x, y, button_config["width"], button_config["height"]
            )
            is_disabled = player.stamina < button["cost"]

            color = (
                config.colors["disabled_button"] if is_disabled else config.colors["button"]
            )
            if is_hovered and not is_disabled:
                color = config.colors["hovered_button"]

            pygame.draw.rect(
                screen,
                color,
                (x, y, button_config["width"], button_config["height"]),
                border_radius=10,
            )
            button_text = font.render(button["label"], True, config.colors["text"])
            button_text_rect = button_text.get_rect(
                center=(
                    x + button_config["width"] // 2,
                    y + button_config["height"] // 2,
                )
            )
            screen.blit(button_text, button_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button, (x, y) in zip(buttons, button_config["positions"]):
                    if is_mouse_over_button(
                        mouse_x,
                        mouse_y,
                        x,
                        y,
                        button_config["width"],
                        button_config["height"],
                    ):
                        if player.stamina >= button["cost"]:
                            return button["action"]
