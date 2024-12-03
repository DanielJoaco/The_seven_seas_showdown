# Manual de Usuario: **The Seven Seas Showdown**

Bienvenido a **The Seven Seas Showdown**, un juego de batalla naval interactivo en el que los jugadores se enfrentan contra un bot. A continuación, te presentamos cómo jugar, las reglas y las funciones del juego.

## **1. Introducción**

En este juego, tendrás que colocar tus barcos en un tablero, lanzar ataques y defenderte con un escudo para sobrevivir. La mecánica está basada en un sistema de turnos, donde tanto el jugador como el bot se alternan para atacar y defenderse.

## **2. Requisitos del Sistema**

- **Sistema Operativo**: Windows, Linux, macOS.
- **Python**: Se requiere tener Python 3.x instalado.
- **Dependencias**:
  - Pygame 2.x (para la interfaz gráfica)
  - Archivos de recursos (sonidos, imágenes y fuentes)

## **3. Iniciando el Juego**

### **3.1 Pantalla de Menú Principal**

Cuando inicies el juego, verás un menú principal con las siguientes opciones:

1. **Start Game**: Iniciar una nueva partida.
2. **Show Rules**: Ver las reglas del juego.
3. **Show Settings**: Configurar algunos parámetros del juego (como el tamaño del tablero).
4. **Exit**: Salir del juego.

Usa las teclas de flechas o el mouse para navegar por las opciones y presiona **Enter** para confirmar la selección.

### **3.2 Comenzando una Nueva Partida**

Al elegir **Start Game**, serás llevado a una pantalla donde podrás colocar tus barcos en el tablero. Aquí es donde podrás elegir el tamaño de los barcos y su orientación. Para colocar un barco, selecciona una celda en el tablero y presiona **Enter** para confirmar. El bot colocará sus barcos automáticamente.

## **4. Mecánicas del Juego**

### **4.1 Colocación de Barcos**

- **Paso 1**: Coloca tus barcos en el tablero. Elige un barco de la flota y selecciona la posición para colocarlo. Los barcos pueden colocarse de manera horizontal o vertical.
- **Paso 2**: Si colocas un barco en una posición inválida, se te mostrará un mensaje indicándote el error.

### **4.2 Turnos de Juego**

El juego se desarrolla en turnos. Cada jugador (y el bot) tiene un turno para atacar. Los turnos se desarrollan de la siguiente manera:

1. **Turno del Jugador**:
   - El jugador puede realizar uno de los siguientes ataques: ataque normal, ataque en línea, ataque cuadrado, o activar un escudo.
   - Si el jugador ataca exitosamente un barco enemigo, el tablero mostrará un **color de impacto** (`#E55812`).
   - Si el jugador falla en el ataque, el tablero mostrará un **color de agua** (`#696969`).
   - Si el jugador usa un escudo, este bloquea el próximo ataque del enemigo.

2. **Turno del Bot**:
   - El bot realiza ataques aleatorios contra el jugador.
   - Los ataques del bot también pueden ser exitosos o fallar. El bot tiene una posibilidad de usar un escudo.
   
### **4.3 Ataques Especiales**

- **Ataque Normal**: Un ataque básico que no consume estamina.
- **Ataque Lineal**: Un ataque en línea de 3 celdas.
- **Ataque Cuadrado**: Un ataque en forma de cuadro que afecta 4 celdas.
- **Escudo**: El jugador puede activar un escudo para protegerse de un ataque. El escudo bloquea un solo ataque, pero consume estamina.

### **4.4 Finalización del Juego**

El juego termina cuando uno de los jugadores pierde toda su vida (es decir, cuando todos sus barcos han sido hundidos). Se muestra una pantalla de victoria donde se indica el ganador.

## **5. Colores en el Juego**

Los colores en el juego indican los estados de las celdas y los ataques realizados:

- **Color de Celdas**:
  - **Agua No Atacada**: `#163040`
  - **Agua Atacada** (fallo): `#696969`
  - **Barco Atacado** (impacto): `#E55812`
  - **Escudo**: `#00008B`

- **Color de Ataques**:
  - **Ataque Exitoso**: `#E55812` (color de impacto).
  - **Ataque Fallido**: `#696969` (agua).
  - **Escudo Bloqueado**: `#00008B` (escudo activado).

## **6. Controles**

### **6.1 Teclado**

- **Flechas**: Navegar por el menú o el tablero.
- **Enter**: Confirmar selección.
- **Esc**: Salir o regresar al menú principal.

### **6.2 Ratón**

- **Clic Izquierdo**: Seleccionar opciones y colocar barcos.
- **Clic Derecho**: Rotar los barcos (horizontal/vertical).

## **7. Reglas del Juego**

### **7.1 Colocación de Barcos**
1. Coloca tus barcos en el tablero.
2. Cada barco debe tener una posición válida y no puede superponerse con otro barco.

### **7.2 Fase de Ataque**
1. El jugador y el bot se alternan para atacar.
2. Un ataque puede tener éxito (golpear un barco) o fallar (agua).
3. Se puede activar un escudo para bloquear un ataque.

### **7.3 Condiciones de Victoria**
El primer jugador que hunde todos los barcos del oponente gana la partida.

## **8. Solución de Problemas**

- **El juego no se inicia**: Asegúrate de tener todas las dependencias instaladas correctamente (Pygame, archivos de recursos).
- **Problemas con los controles**: Asegúrate de estar usando las teclas o el ratón correctamente según se indique.

## **9. Créditos**

Este juego ha sido desarrollado por **Daniel Joaco**, utilizando Pygame y Python.

## **10. Contacto**

Si tienes alguna pregunta o sugerencia, puedes ponerte en contacto con nosotros a través de **daneiljorjuela@gmail.com**.
