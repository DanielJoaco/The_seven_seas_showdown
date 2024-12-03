import pygame
import random
from modules.buttons import draw_button, is_mouse_over_button
from modules.config import config

def dice_turn(screen, message, button_area_rect):
    """
    Lógica para lanzar el dado con un botón dentro del área central.
    """
    font = pygame.font.Font(config.font_regular, 24)

    button_config = {
        "x": button_area_rect.x + 100,
        "y": button_area_rect.y + 80,
        "width": 200,
        "height": 50,
    }

    dice_result = None
    rolling = False
    start_time = None
    clock = pygame.time.Clock()

    while dice_result is None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered = is_mouse_over_button(
            mouse_x,
            mouse_y,
            button_config["x"],
            button_config["y"],
            button_config["width"],
            button_config["height"],
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and is_hovered
            ):
                rolling = True
                start_time = pygame.time.get_ticks()

        dice_result = _render_dice_turn(
            screen,
            font,
            button_area_rect,
            rolling,
            start_time,
            message,
            button_config,
            is_hovered,
        )

        pygame.display.flip()
        clock.tick(60)

    return dice_result

def _render_dice_turn(
    screen, font, button_area_rect, rolling, start_time, message, button_config, is_hovered
):
    """
    Renderiza la sección del dado, maneja la animación y el mensaje.
    """
    pygame.draw.rect(
        screen, config.colors["background"], button_area_rect, border_radius=10
    )

    if rolling:
        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time < 3000:
            current_roll = random.randint(1, 100)
            message = str(current_roll)
        else:
            return random.randint(1, 100)

    message_text = font.render(message, True, config.colors["text"])
    message_text_rect = message_text.get_rect(
        center=(button_area_rect.centerx, button_area_rect.centery - 40)
    )
    screen.blit(message_text, message_text_rect)

    draw_button(
        screen,
        button_config["x"],
        button_config["y"],
        button_config["width"],
        button_config["height"],
        "Tirar Dado",
        font,
        is_hovered=is_hovered,
    )
    return None

def process_dice_roll(dice_result, player):
    """
    Maneja el resultado del dado, aplica efectos al jugador y devuelve un mensaje para la interfaz.
    """
    event = _get_dice_event(dice_result)
    event["action"](player)
    print(f"Resultado del dado: {dice_result} -> {event['message']}")
    return event["message"]

def _get_dice_event(dice_result):
    """
    Obtiene el evento del dado basado en el rango del resultado.
    """
    dice_events = [
        {"range": range(1, 6), "action": lambda p: setattr(p, "turn_skipped", True), "message": "Pierde turno."},
        {"range": range(6, 36), "action": lambda p: setattr(p, "stamina", p.stamina + 1), "message": "Ganas 1 punto de estamina."},
        {"range": range(36, 46), "action": lambda p: setattr(p, "stamina", p.stamina + 2), "message": "Gana 2 puntos de estamina."},
        {"range": range(46, 51), "action": lambda p: setattr(p, "stamina", p.stamina + 3), "message": "Gana 3 puntos de estamina."},
        {"range": range(51, 56), "action": lambda p: setattr(p, "life", max(0, p.life - 1)), "message": "Pierde 1 de vida."},
        {"range": range(56, 96), "action": lambda p: None, "message": "No pasa nada."},
        {"range": range(96, 101), "action": lambda p: setattr(p, "temp_shield", True), "message": "Obtiene un escudo"},
    ]

    for event in dice_events:
        if dice_result in event["range"]:
            return event

    return {"action": lambda p: None, "message": "Evento desconocido."}
