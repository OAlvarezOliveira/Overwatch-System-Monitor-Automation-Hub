# 2026-10-09: Fases 1 y 2, monitor de CPU, RAM y disco y servidor WebSocket

## Hecho

- Exploración de `psutil` a mano: PID propio (`os.getpid()`), proceso padre (`Process.parent()`), `cpu_percent`, `virtual_memory` y `disk_usage`.
- Escrito `service/monitor.py`: bucle `while True` que lee CPU, RAM y disco e imprime el porcentaje de cada uno cada 0,5 s.
- Convertida la lectura en la función `leer_metricas()`, que primero devolvía una tupla `(cpu, memoria, disco)` y ahora devuelve un diccionario con las claves `cpu`, `memoria` y `disco`; el bucle solo arranca bajo `if __name__ == "__main__":`, así que el archivo se puede importar sin que se quede colgado.
- Comprobado desde la terminal con el venv: salen CPU, RAM y disco reales (por ejemplo 15,5 %, 36,5 % y 57,4 %).

- Decisiones de la fase 2 registradas en `docs/decisiones.md`: WebSockets, JSON con claves con nombre, intervalo de 0,5 s y `null` para una métrica no disponible.
- Escrito `service/servidor.py`: servidor WebSocket con `websockets` que, por cada cliente conectado, envía `leer_metricas()` convertido a JSON cada 0,5 s. Probado desde la terminal con `python -m websockets ws://localhost:8765`, que recibió las lecturas.
- Pulido del servidor: `asyncio.run(main())` queda bajo `if __name__ == "__main__":`; se captura `ConnectionClosed` (cliente que se va) y `KeyboardInterrupt` (`Ctrl+C`), de modo que ya no salen tracebacks al pararlo ni al desconectar un cliente.
- La medición se hace en otro hilo con `asyncio.to_thread(leer_metricas)` para que no congele a los demás clientes, y se quita `asyncio.sleep(0.5)`. Contado a ojo con dos clientes a la vez: unas 20 líneas en 10 s, es decir, 0,5 s reales de intervalo (antes eran unos 1,0 s).
- Primer test automático (`service/tests/test_monitor.py`, con `pytest.ini` y `pytest` en `requirements.txt`): comprueba que `leer_metricas()` devuelve exactamente las claves `cpu`, `memoria` y `disco`. Visto fallar a propósito (cambiando `disco` por `disko`) y volver a verde.
- Decisión de arquitectura registrada: `monitor.py` no importa nunca `servidor.py`, estructura plana por ahora y nombres en `snake_case`; la función del servidor pasó a llamarse `iniciar_lectura_metricas`.

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
- **`async def` no basta si dentro bloqueas:** `cpu_percent(interval=0.5)` congela el programa entero medio segundo. `asyncio.to_thread(funcion)` (sin paréntesis en la función y con `await`) la ejecuta en otro hilo.
- **Sumar esperas duplica el intervalo:** `cpu_percent(interval=0.5)` ya marca el ritmo; con un `sleep(0.5)` más, cada vuelta duraba 1 s. Hubo un diagnóstico erróneo al principio (se esperaban 20 líneas con la versión antigua): conviene medir antes de explicar.
- **`try/except` captura lo esperado:** `ConnectionClosed` dentro del bucle del cliente y `KeyboardInterrupt` alrededor de `asyncio.run`.
- **Un test con solo `pass` siempre pasa.** Un test fiable se ha visto fallar al menos una vez. `set(diccionario)` compara solo las claves.
- **Dependencias en un solo sentido** entre módulos: facilita probar `monitor.py` sin servidor y evita importaciones circulares.
- **La terminal puede perder teclas** al pegar texto (marcas `^[[200~`); escribir a mano y, si se atasca, abrir una pestaña nueva. En una pestaña nueva hay que activar el venv (`source .venv/bin/activate`) antes de usar `python`.
- **Guardar en el editor:** varias veces el archivo no estaba guardado o se guardó fuera de `tests/`; se comprueba con `ls -l` y la hora de modificación.

## Pendiente

- Salida más cómoda de leer (una línea por lectura).
- Cada cliente tiene su propio bucle y su propia medición de CPU; con muchos clientes habría que medir una vez y difundir a todos.
- La métrica no disponible (`null`) está decidida pero no implementada.
- Más tests (formato del mensaje enviado, comportamiento del servidor).
- Verificación independiente de las fases 1 y 2 antes de darlas por cerradas; la medición de intervalo se hizo contando a ojo.

## Siguiente

- Fase 3: dashboard de Kotlin conectado a este servidor (requiere instalar Kotlin y Gradle con SDKMAN).
