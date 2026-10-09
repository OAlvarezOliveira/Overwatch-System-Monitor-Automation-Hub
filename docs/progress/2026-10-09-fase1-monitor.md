# 2026-10-09: Fase 1, primer monitor de CPU, RAM y disco

## Hecho

- Exploración de `psutil` a mano: PID propio (`os.getpid()`), proceso padre (`Process.parent()`), `cpu_percent`, `virtual_memory` y `disk_usage`.
- Escrito `service/monitor.py`: bucle `while True` que lee CPU, RAM y disco e imprime el porcentaje de cada uno cada 0,5 s.
- Convertida la lectura en la función `leer_metricas()`, que devuelve `(cpu, memoria, disco)`; el bucle solo arranca bajo `if __name__ == "__main__":`, así que el archivo se puede importar sin que se quede colgado.
- Comprobado desde la terminal con el venv: salen CPU, RAM y disco reales (por ejemplo 15,5 %, 36,5 % y 57,4 %).

- Decisiones de la fase 2 registradas en `docs/decisiones.md`: WebSockets, JSON con claves con nombre, intervalo de 0,5 s y `null` para una métrica no disponible.
- Escrito `service/servidor.py`: servidor WebSocket con `websockets` que, por cada cliente conectado, envía `leer_metricas()` convertido a JSON cada 0,5 s. Probado desde la terminal con `python -m websockets ws://localhost:8765`, que recibió las lecturas.

## Aprendido

- **`async`/`await`:** una función `async def` puede ceder el turno mientras espera (`await asyncio.sleep`), de modo que un servidor atiende a varios clientes a la vez.
- **Pasar una función no es llamarla:** `send(leer_metricas)` entrega la función; `send(leer_metricas())` entrega su resultado.
- **`send` solo manda texto:** el diccionario se convierte antes con `json.dumps`.
- **Spyder (Flatpak) no ve las librerías del `.venv`:** `websockets` solo existe en el venv, así que el servidor se ejecuta desde la terminal.
- **Función y `return`:** devolver los valores en lugar de imprimirlos permite reutilizarlos (la fase 2 los enviará por red).
- **`if __name__ == "__main__":`** separa «lo que ocurre al ejecutar el archivo» de «lo que ocurre al importarlo».
- **Proceso y padre:** cada proceso lo lanza otro. En la terminal la cadena es `python` ← `zsh` ← `herdr`.
- **`cpu_percent()` mide desde la llamada anterior.** Sin `interval` la primera lectura no es fiable (daba 0,0). Con `interval=0.5` espera medio segundo y mide ese tramo, lo que además fija el ritmo del bucle.
- **`percent` ya es un porcentaje.** `used` está en bytes.
- **En un archivo `.py` hace falta `print`.** Una expresión suelta solo se muestra en la consola interactiva.
- **Sangría:** en Python define qué líneas pertenecen al bucle.
- **Spyder instalado desde la tienda de Pop!_OS es un Flatpak** (la cadena de procesos termina en `bwrap`). Corre en una caja aislada: su `"/"` es el de la caja y `disk_usage("/")` daba 0,0 en lugar de 57,4. Para medir el sistema real, el servicio se ejecuta desde la terminal con `service/.venv`.

## Pendiente

- Salida más cómoda de leer (una línea por lectura).
- Que el servidor envíe a todos los clientes a la vez (ahora cada cliente tiene su propio bucle).
- Manejar bien la desconexión de un cliente y la métrica no disponible (`null`).
- Verificación independiente de la fase 1 antes de darla por cerrada.

## Siguiente

- Terminar la fase 2 y empezar el dashboard de Kotlin (fase 3) conectándolo a este servidor.
