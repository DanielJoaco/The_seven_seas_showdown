# Análisis del Proyecto: **The Seven Seas Showdown**

## **1. Introducción**

**The Seven Seas Showdown** es un juego de batalla naval interactivo donde el jugador compite contra un bot. El juego se desarrolla en un entorno gráfico utilizando **Pygame** y Python, y se basa en mecánicas de turnos donde ambos jugadores (el humano y el bot) se alternan para realizar ataques y defenderse utilizando barcos y escudos. 

El proyecto involucra aspectos clave como la gestión de recursos (estamina), la lógica de los turnos, la interacción con la interfaz gráfica y la implementación de funcionalidades complejas como los ataques en línea, ataques cuadrados y el uso de escudos.

Este análisis detalla las decisiones tomadas durante el desarrollo del proyecto, la estructura de sus módulos, las interacciones entre ellos y las mecánicas implementadas.

## **2. Objetivos del Proyecto**

El objetivo principal del proyecto es crear un juego de batalla naval que sea entretenido, desafiante y educativo, con una interfaz gráfica interactiva y una IA (inteligencia artificial) que haga de adversario al jugador. Además, el proyecto busca promover el uso de buenas prácticas de programación, como la modularización del código y la reutilización de funciones.

## **3. Estructura del Proyecto**

El proyecto se organiza en varios módulos que separan las responsabilidades y facilitan la gestión del código. A continuación se describe cada uno:

### **3.1 Módulo `config.py`**

Este módulo contiene todas las configuraciones globales del juego, como las dimensiones de la ventana, los colores, las rutas a los recursos (imágenes, sonidos, fuentes) y otros parámetros configurables (por ejemplo, el tamaño del tablero y las posiciones de inicio). La clase `Config` permite centralizar todos los ajustes importantes, facilitando la gestión y posibles modificaciones.

#### **Responsabilidades**:
- Configurar la pantalla de juego (tamaño de la ventana, título, icono).
- Definir los colores que se usan en el juego para diferentes elementos (tablero, texto, impacto de ataques).
- Almacenar las rutas de los recursos (imágenes, sonidos, fuentes).

### **3.2 Módulo `board.py`**

Este módulo maneja la lógica del tablero de juego. Se encarga de crear el tablero, representar los barcos y los estados de las celdas (agua, impacto, escudo), y gestionar la actualización de las celdas según los ataques.

#### **Responsabilidades**:
- Crear y gestionar el tablero del jugador y el bot.
- Determinar el estado de cada celda (agua, impacto, escudo).
- Dibujar el tablero en pantalla.

### **3.3 Módulo `player.py`**

El módulo `player.py` define la clase `Player`, que representa tanto al jugador como al bot en el juego. Cada jugador tiene un conjunto de barcos (flota), puntos de vida (vida) y estamina, y puede realizar diferentes tipos de ataques (normal, en línea, cuadrado) y activar un escudo.

#### **Responsabilidades**:
- Gestionar los barcos del jugador (colocación, verificación de posiciones válidas).
- Controlar los puntos de vida y la estamina.
- Recibir ataques y actualizar el estado de los barcos.
- Realizar ataques (normal, en línea, cuadrado) y gestionar el uso del escudo.

### **3.4 Módulo `ui.py`**

Este módulo se encarga de la interfaz gráfica del juego. Controla la pantalla, dibuja los tableros, los botones del menú y las interacciones con el usuario. Además, se encarga de mostrar los textos (como los mensajes de ataque y las instrucciones).

#### **Responsabilidades**:
- Inicializar la pantalla de juego.
- Dibujar el estado del juego (tableros, información del jugador).
- Gestionar la interfaz del menú (pantalla principal, opciones, etc.).
- Mostrar mensajes y textos informativos en pantalla.

### **3.5 Módulo `game_logic.py`**

El módulo `game_logic.py` contiene la lógica principal del flujo del juego, como la colocación de barcos, la gestión de turnos, y el control de las acciones en cada turno (tirar el dado, elegir ataques, etc.).

#### **Responsabilidades**:
- Controlar la colocación de barcos del jugador y el bot.
- Gestionar la fase de ataque (turnos del jugador y del bot).
- Controlar la lógica de las rondas del juego.

### **3.6 Módulo `attacks_logic.py`**

Este módulo maneja las acciones relacionadas con los ataques (normal, en línea, cuadrado) y el uso de escudos. Contiene la lógica de cómo cada tipo de ataque afecta a las celdas del tablero y cómo se calculan los impactos.

#### **Responsabilidades**:
- Manejar las diferentes mecánicas de ataque (normal, línea, cuadrado).
- Determinar los resultados de los ataques (acierto, fallo, escudo).
- Actualizar el estado del tablero tras un ataque.

### **3.7 Módulo `buttons.py`**

Este módulo gestiona los botones de la interfaz, tanto para la navegación en el menú como para las acciones de ataque. Aquí se definen las funciones para dibujar los botones, detectar interacciones del usuario con los botones y realizar las acciones correspondientes.

#### **Responsabilidades**:
- Dibujar los botones del menú y los botones de acción (ataques).
- Detectar cuando el usuario interactúa con un botón y procesar la acción seleccionada.

### **3.8 Módulo `warships.py`**

Este módulo define los barcos (clase `Ship`) y la flota del jugador. Los barcos se colocan en el tablero mediante la función `place`, y la flota se crea en el juego utilizando la función `create_fleet`.

#### **Responsabilidades**:
- Definir la estructura de los barcos y sus posiciones.
- Crear una flota predeterminada de barcos.

### **3.9 Módulo `utils.py`**

Este módulo contiene funciones utilitarias para manejar la interacción con el tablero, la selección de celdas con el ratón y las verificaciones de colocación de barcos. También incluye funciones para mostrar mensajes en pantalla y dibujar una vista previa de los ataques.

#### **Responsabilidades**:
- Dibujar el tablero vacío y manejar las selecciones de celdas.
- Verificar si un barco puede colocarse en una posición válida.
- Dibujar la previsualización de la colocación de barcos y ataques.

## **4. Funcionalidades Implementadas**

### **4.1 Colocación de Barcos**
Los jugadores y el bot colocan sus barcos en el tablero antes de comenzar la fase de ataques. La colocación es validada para asegurarse de que los barcos no se solapen y estén dentro del tablero.

### **4.2 Fase de Ataque**
Durante la fase de ataque, los jugadores pueden seleccionar celdas en el tablero enemigo para realizar un ataque. Dependiendo del tipo de ataque seleccionado (normal, en línea o cuadrado), los resultados se procesan de manera diferente. Los jugadores también pueden usar un escudo para bloquear un ataque del bot.

### **4.3 Resultados de Ataques**
Cuando un jugador o el bot realizan un ataque, el estado de la celda en el tablero cambia dependiendo de si el ataque fue exitoso, fallido o bloqueado por un escudo.

### **4.4 Lógica de Turnos**
El juego sigue una secuencia de turnos donde los jugadores y el bot se alternan para atacar. Si un jugador o el bot activan un escudo, pueden atacar nuevamente sin cambiar el turno.

### **4.5 Condiciones de Victoria**
El juego termina cuando todos los puntos de vida de un jugador (ya sea el jugador o el bot) llegan a cero, indicando que todos los barcos han sido destruidos.

## **5. Desafíos y Soluciones**

### **5.1 Coordinación de la IA del Bot**
Uno de los principales desafíos fue desarrollar una IA de bot que fuera desafiante pero justa. Para ello, se implementaron ataques aleatorios y el uso de un escudo para bloquear ataques, lo que da al bot una ventaja estratégica.

### **5.2 Gestión de Recursos (Estamina)**
La estamina juega un papel crucial en la dinámica de los ataques especiales (como el ataque en línea y cuadrado). Se implementó una lógica para asegurar que los ataques especiales solo pudieran realizarse si el jugador o el bot tenían suficiente estamina.

### **5.3 Diseño de la Interfaz Gráfica**
La interfaz gráfica fue diseñada para ser intuitiva, mostrando claramente el estado del juego, los tableros de ambos jugadores y las opciones de ataque disponibles. También se implementó un sistema de menús para facilitar la navegación y selección de opciones.

## **6. Conclusiones**

**The Seven Seas Showdown** es un juego divertido y desafiante que combina estrategia y elementos de azar (como los ataques aleatorios del bot y el uso del dado). La implementación modular del proyecto permite que las distintas partes del juego (lógica, interfaz, IA) estén bien separadas, lo que facilita la extensión y el mantenimiento del código.

El juego es ideal para aquellos interesados en juegos de estrategia con mecánicas de ataque y defensa, y ofrece una buena base para experimentar con diferentes tipos de IA y mecánicas de juego adicionales en el futuro.

## **7. Posibles Mejoras**
- **Mejora de la IA**: Implementar una IA más avanzada que no se limite a atacar aleatoriamente, sino que considere las acciones del jugador y las posiciones de los barcos.
- **Multijugador**: Agregar una opción de juego multijugador en línea para permitir que dos jugadores se enfrenten en vez de jugar contra un bot.
- **Mejoras en los gráficos**: Mejorar los efectos visuales durante los ataques y cuando los barcos sean hundidos, para hacer el juego más dinámico y visualmente atractivo.

---
