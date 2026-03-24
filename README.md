# Contador de palabras en repositorios de GitHub (Python y Java)

Repositorio con tarea de diagnostico de ingenieria de datos para contar palabras en nombres de funciones y metodos de repositorios de GitHub (Python y Java).

## Arquitectura: Productor-Consumidor

El sistema sigue un modelo de arquitectura **Productor–Consumidor** desacoplado mediante una base de datos Redis y esta desarrallodo utilizando Python, se compone de:

1.  **Miner (Productor)**: Crawlea GitHub utilizando la API de GitHub buscando repositorios populares (por cantidad de estrellas), extrae los nombres de funciones/métodos y los descompone en palabras, enviando las frecuencias a Redis. Luego se analiza cada archivo .py y .java para extraer los nombres de funciones y métodos.
2.  **Redis (Broker/Almacenamiento)**: Actúa como el canal de comunicación en tiempo real y almacenamiento persistente de los conteos (usando un *Sorted Set*).
3.  **Visualizer (Consumidor)**: Aplicación web simple en Streamlit que lee los datos desde Redis y genera visualizaciones en tiempo real.

## Ejecución:

1.  Clona el repositorio.
2.  Crea un archivo `.env` en la raíz del proyecto:
    ```env
    GITHUB_TOKEN=tu_token_de_github_aqui
    ```
3.  Buildea y ejecuta los contenedores:
    ```bash
    docker-compose up --build
    ```
4.  Accede al **Visualizer** en: [http://localhost:8501](http://localhost:8501).





