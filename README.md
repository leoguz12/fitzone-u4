# FitZone - API de Reservas (Actividad 4)

Este proyecto es una API REST desarrollada con **FastAPI** implementando los patrones de Diseño Orientado al Dominio (DDD) para el gimnasio FitZone. Se gestiona la máquina de estados de las reservas de los socios y la validación de reglas de negocio para promociones.

## Tecnologías Utilizadas
* Python 3.11+
* FastAPI & Uvicorn (Servidor web)
* Pytest (Pruebas unitarias)
* Patrones DDD: Entidades, Value Objects, Aggregate Roots, Domain Events y Specifications.

## Instalación y Ejecución

1. Activar el entorno virtual:
   .venv\Scripts\activate

2. Instalar las dependencias:
   py -m pip install fastapi uvicorn pytest httpx

3. Levantar el servidor:
   py -m uvicorn app.api:app --reload

4. La documentación interactiva (Swagger) estará disponible en:
   http://127.0.0.1:8000/docs

## Pruebas Automáticas
Para ejecutar la batería de pruebas y validar las reglas de negocio, utiliza:
py -m pytest -q