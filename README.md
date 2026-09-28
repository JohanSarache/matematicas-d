# Matemáticas D

Repositorio de la asignatura **Matemáticas D**, organizado por temas, ejercicios y ejemplos desarrollados principalmente en **Python**.

El proyecto utiliza **Docker** para mantener un entorno reproducible y evitar problemas de versiones o dependencias entre diferentes computadoras.

## Tecnologías

- Python 3.12
- NumPy
- SciPy
- SymPy
- Matplotlib
- Pandas
- JupyterLab
- Docker
- Docker Compose
- Git
- GitHub

## Estructura del proyecto

La estructura general del repositorio es:

```text
matematicas-d/
├── temas/
├── recursos/
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

Los contenidos se organizarán por tema. Por ejemplo:

```text
temas/
└── 01_interpolacion/
    ├── README.md
    ├── ejercicios/
    │   ├── ejercicio_01.py
    │   └── ejercicio_02.py
    ├── notebooks/
    └── datos/
```

Cada tema podrá contener:

- `README.md`: descripción y contenido del tema.
- `ejercicios/`: ejercicios desarrollados principalmente en Python.
- `notebooks/`: notebooks de Jupyter cuando resulte útil trabajar de forma interactiva.
- `datos/`: archivos de datos utilizados por los ejercicios del tema.

Los archivos `.py` serán el formato principal de trabajo. JupyterLab quedará disponible como herramienta complementaria cuando resulte conveniente.

## Construir el entorno

Después de clonar el repositorio, ingresar al directorio del proyecto:

```bash
cd matematicas-d
```

Construir la imagen Docker:

```bash
docker compose build
```

Este comando crea el entorno de trabajo e instala las dependencias definidas en `requirements.txt`.

## Ejecutar un script Python

Los ejercicios desarrollados como archivos `.py` pueden ejecutarse directamente dentro del entorno Docker.

Formato general:

```bash
docker compose run --rm matematicas python ruta/al/script.py
```

Por ejemplo:

```bash
docker compose run --rm matematicas python temas/01_interpolacion/ejercicios/ejercicio_01.py
```

La opción `--rm` elimina automáticamente el contenedor temporal una vez que finaliza la ejecución del script.

De esta manera no es necesario instalar localmente Python, NumPy, SciPy, SymPy u otras dependencias del proyecto.

## JupyterLab

JupyterLab está disponible para aquellos temas donde resulte conveniente trabajar de forma interactiva.

Para iniciarlo:

```bash
docker compose up
```

JupyterLab estará disponible normalmente en:

```text
http://127.0.0.1:8888
```

La terminal mostrará la dirección de acceso y, cuando corresponda, el token necesario para ingresar.

Para detener el entorno puede utilizarse:

```text
Ctrl + C
```

o, desde otra terminal:

```bash
docker compose down
```