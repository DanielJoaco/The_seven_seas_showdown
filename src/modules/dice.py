import pygame
import random
from modules.buttons import draw_button, is_mouse_over_button
from modules.config import config

def dice_turn(screen, message, button_area_rect, process_dice_roll):
    """
    Lógica para lanzar el dado con un botón dentro del área central.
    """
    button_x = button_area_rect.x + 50
    button_y = button_area_rect.y + 100
    button_width = 200
    button_height = 50

    font = pygame.font.Font(config.font_regular, 24)

    dice_result = None
    rolling = False
    start_time = None
    clock = pygame.time.Clock()

    while dice_result is None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered = is_mouse_over_button(mouse_x, mouse_y, button_x, button_y, button_width, button_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    if is_hovered:
                        rolling = True
                        start_time = pygame.time.get_ticks()

        # Dibujar la sección central
        pygame.draw.rect(screen, config.colors["background"], button_area_rect, border_radius=10)

        # Mostrar el mensaje o el resultado temporal del dado
        if rolling:
            elapsed_time = pygame.time.get_ticks() - start_time
            if elapsed_time < 3000:  # Lanzamiento de 3 segundos
                current_roll = random.randint(1, 20)
                message = str(current_roll)  # Reemplaza el mensaje por el número aleatorio
            else:
                dice_result = random.randint(1, 20)
                process_dice_roll(dice_result)

        # Dibujar el mensaje (número o texto)
        message_text = font.render(message, True, config.colors["text"])
        message_rect = message_text.get_rect(center=(button_area_rect.centerx, button_area_rect.centery - 40))
        screen.blit(message_text, message_rect)

        # Crear el botón
        draw_button(
            screen,
            button_x,
            button_y,
            button_width,
            button_height,
            "Tirar Dado",
            font,
            is_hovered=is_hovered
        )

        pygame.display.flip()
        clock.tick(60)

    return dice_result

def draw_dice_area(screen, message, font):
    """
    Dibuja el área donde se muestra el resultado del dado.
    :param screen: Superficie donde se dibuja.
    :param message: Mensaje a mostrar en el área del dado.
    :param font: Fuente del texto.
    """
    dice_area_width = 300
    dice_area_height = 150
    dice_area_x = config.WINDOW_WIDTH // 2 - dice_area_width // 2
    dice_area_y = config.WINDOW_HEIGHT // 2 - dice_area_height // 2 - 200  # Encima del botón

    # Dibujar el área del dado
    pygame.draw.rect(screen, config.colors["background"], (dice_area_x, dice_area_y, dice_area_width, dice_area_height), border_radius=10)
    pygame.draw.rect(screen, config.colors["border"], (dice_area_x, dice_area_y, dice_area_width, dice_area_height), width=2, border_radius=10)

    # Dibujar el texto
    message_text = font.render(message, True, config.colors["text"])
    message_text_rect = message_text.get_rect(center=(dice_area_x + dice_area_width // 2, dice_area_y + dice_area_height // 2))
    screen.blit(message_text, message_text_rect)

def process_dice_roll(dice_result):
    """
    Maneja el resultado del dado y ejecuta acciones basadas en el número obtenido.
    """
    print(f"Resultado del dado: {dice_result}")

    if dice_result <= 5:
        print("Resultado bajo: Activar penalización.")
        # Implementar la penalización aquí.
    elif dice_result <= 15:
        print("Resultado medio: Nada especial ocurre.")
        # Acción neutral aquí.
    else:
        print("Resultado alto: Activar bonificación.")
        # Implementar la bonificación aquí.
