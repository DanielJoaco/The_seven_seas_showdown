import pygame

# Definición de skins de colores
skins = [
    {"name": "Azul Oceánico", "BACKGROUND_COLOR": (72, 106, 219), "CELL_COLOR": (106, 118, 160), "BORDER_COLOR": (58, 51, 48)},
    {"name": "Verde Esmeralda", "BACKGROUND_COLOR": (34, 139, 34), "CELL_COLOR": (50, 205, 50), "BORDER_COLOR": (0, 100, 0)},
    {"name": "Rojo Coral", "BACKGROUND_COLOR": (220, 20, 60), "CELL_COLOR": (255, 105, 97), "BORDER_COLOR": (139, 0, 0)},
]

# Variables de color (inicializadas con el primer skin)
current_skin_index = 0
BACKGROUND_COLOR = skins[current_skin_index]["BACKGROUND_COLOR"]
CELL_COLOR = skins[current_skin_index]["CELL_COLOR"]
BORDER_COLOR = skins[current_skin_index]["BORDER_COLOR"]

def show_settings(screen, WINDOW_WIDTH, WINDOW_HEIGHT, clock):
    global current_skin_index

    font = pygame.font.Font(None, 36)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit", None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RIGHT and current_skin_index < len(skins) - 1:
                    current_skin_index += 1
                elif event.key == pygame.K_LEFT and current_skin_index > 0:
                    current_skin_index -= 1
                elif event.key == pygame.K_RETURN:
                    # Retornar los colores del skin seleccionado y su nombre
                    selected_skin = skins[current_skin_index]
                    return "skin_applied", (selected_skin["BACKGROUND_COLOR"], selected_skin["CELL_COLOR"], selected_skin["BORDER_COLOR"], selected_skin["name"])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, skin in enumerate(skins):
                    skin_rect = pygame.Rect(100 + i * 220, 250, 200, 100)
                    if skin_rect.collidepoint(mouse_x, mouse_y):
                        current_skin_index = i
                        selected_skin = skins[current_skin_index]
                        return "skin_applied", (selected_skin["BACKGROUND_COLOR"], selected_skin["CELL_COLOR"], selected_skin["BORDER_COLOR"], selected_skin["name"])

        # Rellenar la pantalla
        screen.fill(skins[current_skin_index]["BACKGROUND_COLOR"])

        # Título de Configuración
        title_surface = font.render("Seleccione una Skin", True, (255, 255, 255))
        screen.blit(title_surface, ((WINDOW_WIDTH - title_surface.get_width()) // 2, 100))

        # Dibujar skins con previsualización de color
        for i, skin in enumerate(skins):
            skin_rect = pygame.Rect(100 + i * 220, 250, 200, 100)
            if i == current_skin_index:
                pygame.draw.rect(screen, (255, 255, 255), skin_rect, 3)
            pygame.draw.rect(screen, skin["BACKGROUND_COLOR"], skin_rect)
            pygame.draw.rect(screen, skin["CELL_COLOR"], skin_rect.inflate(-20, -20))
            pygame.draw.rect(screen, skin["BORDER_COLOR"], skin_rect, 2)

            # Mostrar el nombre de la skin
            name_surface = font.render(skin["name"], True, (255, 255, 255))
            screen.blit(name_surface, (skin_rect.x + (skin_rect.width - name_surface.get_width()) // 2, skin_rect.y - 30))

        pygame.display.flip()
        clock.tick(60)

    return "canceled", None  # Retorna "canceled" si el usuario sale sin elegir
