# Registro de decisiones

Una entrada por decisión, la más reciente primero. Se escribe con palabras propias:
lo importante es el porqué, porque es lo que se pregunta en una defensa.

## Formato

```
## AAAA-MM-DD: título corto

- **Contexto:** qué problema había y qué restricciones.
- **Opciones:** qué alternativas se consideraron.
- **Decisión:** qué se eligió.
- **Porqué:** el motivo, con los pros y contras que pesaron.
- **Consecuencias:** qué cambia a partir de ahora.
```

## 2026-10-09: Dependencia en un solo sentido entre módulos del servicio

- **Contexto:** el servicio Python tiene tres piezas: `monitor.py` (lee las métricas), `servidor.py` (las envía por WebSocket) y `tests/` (las pruebas). Hay que fijar qué módulo puede importar a cuál.
- **Opciones:** estructura plana con dependencia en un solo sentido; dependencia en ambos sentidos; reestructurar ya en un paquete.
- **Decisión:** `servidor.py` importa `monitor.py`, y `monitor.py` no importa nunca `servidor.py`. Por ahora se mantiene la estructura plana (`service/` con `tests/`). También se adopta `snake_case` para los nombres de funciones, que es la convención de Python (PEP 8).
- **Porqué:** así queda claro cuál depende de cuál.
- **Consecuencias:** `monitor.py` se puede probar sin arrancar ningún servidor (`tests/test_monitor.py` ya lo hace) y se evita un error de importación circular. Cuando lleguen las fases 4 y 5 y haya más módulos, se agruparán en un paquete. Pendiente: la función `iniciarLecturaMetricas` de `servidor.py` sigue en camelCase y hay que renombrarla a `iniciar_lectura_metricas`.

## 2026-10-09: Métrica no disponible, clave presente con `null`

- **Contexto:** algunas métricas pueden no estar disponibles, por ejemplo la temperatura en un equipo sin sensor. Hay que decidir qué recibe el dashboard en ese caso.
- **Opciones:** omitir la clave del mensaje; incluirla con un valor que indique «sin dato» (`null`); incluirla con un valor numérico como `0`.
- **Decisión:** la clave siempre aparece y, cuando no hay dato, su valor es `null` (`None` en Python), por ejemplo `{"cpu": 12.5, "memoria": 37.7, "disco": 57.4, "temperatura": null}`. Se descarta `0` porque sería un dato falso.
- **Porqué:** si no veo la clave no sé si debería disponer de ese dato o no, y puede parecer que todo está correcto y funcionando. Si me falta un dato puede deberse a que no hay hardware para recuperarlo, a un error del mismo o incluso a un problema en el servicio que procesa y envía el dato.
- **Consecuencias:** el dashboard puede distinguir «métrica esperada pero sin dato» de «métrica que no existe» y mostrarlo. El mensaje tiene siempre las mismas claves. Con `null` no se distingue la causa del fallo (sin hardware, error del sensor o fallo del servicio); si hiciera falta, una decisión futura podría añadir un campo de estado o motivo.

## 2026-10-09: Intervalo de muestreo, 0,5 s

- **Contexto:** el servicio lee las métricas en bucle y las envía al dashboard. Hay que fijar cada cuánto se mide y se emite una lectura.
- **Opciones:** intervalos más largos (por ejemplo 5 s) o más cortos (por ejemplo 100 ms) que 0,5 s.
- **Decisión:** 0,5 s. En el código es `psutil.cpu_percent(interval=0.5)`, que mide la CPU durante ese tiempo y marca el ritmo del bucle.
- **Porqué:** porque medio segundo da sensación de tiempo real sin saturar el equipo.
- **Consecuencias:** se emiten unas 2 lecturas por segundo. El valor está escrito en el código; si más adelante se quiere ajustar, conviene sacarlo a una constante o a un parámetro.

## 2026-10-09: Formato del mensaje de métricas, JSON con claves con nombre

- **Contexto:** `leer_metricas()` devolvía una tupla `(cpu, memoria, disco)`. Enviada así por el WebSocket, el dashboard tendría que adivinar qué es cada número por su posición.
- **Opciones:** tupla o lista de números sin nombre; texto JSON con una clave por métrica.
- **Decisión:** `leer_metricas()` devuelve un diccionario con las claves `cpu`, `memoria` y `disco`, y se envía como texto JSON (`json.dumps`), por ejemplo `{"cpu": 10.7, "memoria": 37.8, "disco": 57.4}`.
- **Porqué:** así el dashboard sabe qué es cada valor que Python le envía, y además es un formato estructurado que se mantendrá cuando el servicio necesite crecer.
- **Consecuencias:** añadir una métrica nueva es añadir una clave, sin romper a quien ya lee las demás. Los valores son porcentajes (0 a 100) y la cuestión de qué enviar cuando una métrica no está disponible queda pendiente.

## 2026-10-09: Transporte entre servicio e interfaz, WebSockets

- **Contexto:** el servicio Python y el dashboard son programas distintos, así que las métricas tienen que viajar de uno a otro. El servicio leerá un equipo y enviará los datos a un frontend local.
- **Opciones:** WebSockets o gRPC.
- **Decisión:** WebSockets, por ahora.
- **Porqué:** por complejidad, ahora mismo debe primar la sencillez para aprender y avanzar en el dominio del lenguaje. Además, leer datos de un equipo y enviarlos a un frontend local no es un proceso crítico que vaya a necesitar escalar en seguridad y otras fortalezas que gRPC puede dar.
- **Consecuencias:** el servicio emite una lectura cada intervalo y el dashboard solo escucha. Si más adelante hiciera falta más rigor o rendimiento, la decisión se puede revisar; conviene mantener la lectura (`leer_metricas()`) separada del envío para que el cambio sea barato.

## Decisiones pendientes

Ninguna por ahora. Las decisiones de la fase 2 (transporte, formato, intervalo y métrica no disponible) están registradas arriba.
