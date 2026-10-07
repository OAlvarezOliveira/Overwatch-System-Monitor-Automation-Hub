# 2026-10-07: Reestructuración del repositorio en Linux

## Hecho

- Clonado el repositorio en Pop!_OS, fuera de cualquier otro repositorio.
- Movido `requirements.txt` a `service/` con `git mv`.
- Añadidos `.gitignore`, `README.md` y la carpeta `docs/` (arquitectura, hoja de ruta y diario de progreso).
- Recreado el entorno virtual y reinstalado `psutil` 7.2.2.

## Notas

- `.venv` guarda rutas absolutas, así que se recrea en cada máquina en lugar de moverse.
- Se trabaja en dos equipos (Linux en casa, Windows en clase). Conviene hacer pull al empezar y push al terminar para no divergir.

## Siguiente

- Fase 1: explorar `psutil` a mano y después escribir la función que reúne las métricas de CPU, RAM y disco.
