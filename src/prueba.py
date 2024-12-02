import numpy as np

# Definir las matrices de coeficientes (A) y términos constantes (B)
A = np.array([[3, 6, 9],
              [15, 18, 21],
              [27, 30, 33]])

B = np.array([12, 24, 36])

# Resolver el sistema de ecuaciones
solucion = np.linalg.solve(A, B)

# Mostrar la solución
print("La solución es:")
print(f"x = {solucion[0]}")
print(f"y = {solucion[1]}")
print(f"z = {solucion[2]}")