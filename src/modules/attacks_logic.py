from modules.utils import is_within_bounds

def normal_attack(player, opponent_board, row, col):
    """
    Lógica para el ataque normal: ataca una celda específica.
    """
    result = opponent_board.receive_attack(row, col)
    if result == "hit":
        print(f"Acierto en ({row}, {col})!")
    elif result == "miss":
        print(f"Fallo en ({row}, {col}).")
    elif result == "already_attacked":
        print(f"La celda ({row}, {col}) ya fue atacada.")
    return result


def line_attack(player, opponent_board, row, col):
    """
    Lógica para el ataque lineal: ataca una fila o columna completa.
    """
    if player.stamina < 3:
        return "Estamina insuficiente para ataque lineal."

    player.stamina -= 3
    results = []

    # Ataca la fila completa
    for c in range(opponent_board.board_size):
        results.append(opponent_board.receive_attack(row, c))

    print(f"Ataque lineal realizado en fila {row}.")
    return results


def square_attack(player, opponent_board, row, col):
    """
    Lógica para el ataque cuadrado: ataca un área de 2x2 alrededor de la celda.
    """
    if player.stamina < 4:
        return "Estamina insuficiente para ataque cuadrado."

    player.stamina -= 4
    results = []

    for r in range(row, min(row + 2, opponent_board.board_size)):
        for c in range(col, min(col + 2, opponent_board.board_size)):
            results.append(opponent_board.receive_attack(r, c))

    print(f"Ataque cuadrado realizado en el área de inicio ({row}, {col}).")
    return results


def use_radar(player, opponent_board):
    """
    Lógica para usar el radar: detecta la primera celda ocupada por un barco.
    """
    if player.stamina < 4:
        return "Estamina insuficiente para usar el radar."

    player.stamina -= 4

    for row in range(opponent_board.board_size):
        for col in range(opponent_board.board_size):
            if opponent_board.grid[row][col]["state"] == 1:  # Celda con barco
                print(f"Radar detectó un barco en ({row}, {col}).")
                return f"Barco detectado en ({row}, {col})."

    print("Radar no detectó barcos.")
    return "No se detectaron barcos."


def use_shield(player, ship):
    """
    Lógica para usar un escudo: protege un barco específico.
    """
    if player.stamina < 3:
        return "Estamina insuficiente para colocar un escudo."

    player.stamina -= 3
    ship.has_shield = True
    print(f"Escudo colocado en el barco {ship.name}.")
    return f"Escudo colocado en el barco {ship.name}."


def handle_action(action, player, opponent_board, selected_row=None, selected_col=None):
    """
    Lógica principal para manejar las acciones según el botón seleccionado.
    :param action: Acción seleccionada (normal_attack, line_attack, etc.).
    :param player: Instancia del jugador que realiza la acción.
    :param opponent_board: Tablero del oponente.
    :param selected_row: Fila seleccionada para el ataque.
    :param selected_col: Columna seleccionada para el ataque.
    """
    if action == "normal_attack" and selected_row is not None and selected_col is not None:
        return normal_attack(player, opponent_board, selected_row, selected_col)

    elif action == "line_attack" and selected_row is not None:
        return line_attack(player, opponent_board, selected_row, 0)  # Ataca toda la fila

    elif action == "square_attack" and selected_row is not None and selected_col is not None:
        return square_attack(player, opponent_board, selected_row, selected_col)

    elif action == "use_radar":
        return use_radar(player, opponent_board)

    elif action == "use_shield":
        # Se asume que el jugador debe seleccionar un barco de su flota
        for ship in player.fleet:
            if not ship.has_shield:  # Busca el primer barco sin escudo
                return use_shield(player, ship)
        return "Todos los barcos ya tienen escudo activo."

    else:
        print(f"Acción desconocida o parámetros insuficientes: {action}.")
        return "Acción inválida."
