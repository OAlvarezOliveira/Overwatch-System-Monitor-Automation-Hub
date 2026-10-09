# 2026-10-09: Fase 1, primer monitor de CPU, RAM y disco

## Hecho

- Exploración de `psutil` a mano: PID propio (`os.getpid()`), proceso padre (`Process.parent()`), `cpu_percent`, `virtual_memory` y `disk_usage`.
- Escrito `service/monitor.py`: bucle `while True` que lee CPU, RAM y disco e imprime el porcentaje de cada uno cada 0,5 s.
- Comprobado desde la terminal con el venv: salen CPU, RAM y disco reales (por ejemplo 15,5 %, 36,5 % y 57,4 %).

## Aprendido

- **Proceso y padre:** cada proceso lo lanza otro. En la terminal la cadena es `python` ← `zsh` ← `herdr`.
- **`cpu_percent()` mide desde la llamada anterior.** Sin `interval` la primera lectura no es fiable (daba 0,0). Con `interval=0.5` espera medio segundo y mide ese tramo, lo que además fija el ritmo del bucle.
- **`percent` ya es un porcentaje.** `used` está en bytes.
- **En un archivo `.py` hace falta `print`.** Una expresión suelta solo se muestra en la consola interactiva.
- **Sangría:** en Python define qué líneas pertenecen al bucle.
- **Spyder instalado desde la tienda de Pop!_OS es un Flatpak** (la cadena de procesos termina en `bwrap`). Corre en una caja aislada: su `"/"` es el de la caja y `disk_usage("/")` daba 0,0 en lugar de 57,4. Para medir el sistema real, el servicio se ejecuta desde la terminal con `service/.venv`.

## Pendiente

- Salida más cómoda de leer (una línea por lectura).
- Pasar la lectura a una función reutilizable, paso previo a enviarla por red en la fase 2.
- Verificación independiente de la fase 1 antes de darla por cerrada.

## Siguiente

- Fase 2: decidir el transporte (WebSockets o gRPC) y el formato del mensaje, y registrarlo en `docs/decisiones.md`.
