# The Seven Seas Showdown

The Seven Seas Showdown es un juego interactivo que simula batallas entre barcos en el mar. El objetivo es implementar la lógica de ataque, defensa, y otras características dentro de un entorno de juego donde los jugadores pueden interactuar con el juego de manera dinámica.

## Descripción

Este proyecto es un juego basado en turnos donde los jugadores controlan barcos y deben enfrentarse en batallas. El juego incluye varias mecánicas como ataques, escudos y un sistema de lógica de colisiones. Los jugadores pueden recibir ataques y defenderse utilizando escudos. Este juego está desarrollado en Python utilizando **Pygame** para la parte gráfica y **unittest** para pruebas automatizadas.

## Características

- **Lógica de ataques**: Los jugadores pueden atacar a otros barcos. La lógica de los ataques tiene en cuenta los escudos de los barcos.
- **Escudos**: Los barcos pueden activar un escudo para defenderse de los ataques.
- **Modularidad**: El juego está dividido en varios módulos que permiten la expansión y personalización de las reglas.
- **Pruebas automatizadas**: Se han implementado pruebas para garantizar que la lógica de juego funcione correctamente (usando `unittest`).

## Instalación

### Requisitos previos

- Python 3.11 o superior
- Pygame 2.6.1
- Un sistema operativo compatible (Windows, Linux, macOS)

### Pasos de instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/Seven-Seas-Showdown.git
2. Navega al directorio del proyecto:
    ```bash
    cd Seven-Seas-Showdown
    ```
3. Crea y activa un entorno virtual (opcional, pero recomendado):
    ```bash
    python -m venv env
    source env/bin/activate  # En Linux o macOS
    .\env\Scripts\activate  # En Windows
    ```
4. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

### Ejecutar el juego
Para iniciar el juego, simplemente ejecuta el archivo ````main.py````:

```bash
python src/main.py
```
Este comando abrirá la ventana gráfica del juego, donde podrás interactuar con el entorno y jugar.
### Ejecutar pruebas automatizadas
Para ejecutar las pruebas automatizadas utilizando ```unittest```, usa el siguiente comando:
```bash
python -m unittest discover -s tests
```
Esto buscará y ejecutará todas las pruebas dentro de la carpeta ```tests```.
## Estructura del Proyecto
El proyecto tiene la siguiente estructura de directorios:
```bash
Seven-Seas-Showdown/
├── assets/               # Multimedia del juego
│   ├── fonts/            # 
│   ├── images/
│   ├── sounds/
├── docs/                 #Documentacion del juego
├── src/                  # Código fuente del juego
│   ├── main.py           # Entrada principal del juego
│   ├── modules/          # Módulos del juego (lógica de ataques, movimiento, etc.)
│   └── ...
├── tests/                # Archivos de prueba
│   ├── test_attacks_logic.py
│   ├── test_player.py    # Pruebas del comportamiento de los jugadores
│   └── ...
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Este archivo
```
## Contribuciones
Si deseas contribuir a este proyecto, sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una nueva rama para tus cambios (```git checkout -b feature-nueva-funcionalidad```).
3. Haz tus cambios y haz un commit de los mismos (```git commit -am 'Añadida nueva funcionalidad'```).
4. Envía tus cambios al repositorio original (```git push origin feature-nueva-funcionalidad```).
5. Abre un pull request para que podamos revisar y fusionar tus cambios.
## Licencia
Este proyecto está bajo la Licencia MIT. Para más detalles, consulta [Licencia MIT](https://es.wikipedia.org/wiki/Licencia_MIT).
## Contacto
Si tienes alguna pregunta o sugerencia, no dudes en abrir un issue o contactar al mantenedor:
- Nombre del Mantenedor: Daniel Orjuela
- Correo electrónico: danieljorjuela@gmail.com
- GitHub: danieljoaco

