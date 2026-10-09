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

## 2026-10-09: Transporte entre servicio e interfaz, WebSockets

- **Contexto:** el servicio Python y el dashboard son programas distintos, así que las métricas tienen que viajar de uno a otro. El servicio leerá un equipo y enviará los datos a un frontend local.
- **Opciones:** WebSockets o gRPC.
- **Decisión:** WebSockets, por ahora.
- **Porqué:** por complejidad, ahora mismo debe primar la sencillez para aprender y avanzar en el dominio del lenguaje. Además, leer datos de un equipo y enviarlos a un frontend local no es un proceso crítico que vaya a necesitar escalar en seguridad y otras fortalezas que gRPC puede dar.
- **Consecuencias:** el servicio emite una lectura cada intervalo y el dashboard solo escucha. Si más adelante hiciera falta más rigor o rendimiento, la decisión se puede revisar; conviene mantener la lectura (`leer_metricas()`) separada del envío para que el cambio sea barato.

## Decisiones pendientes

- Formato de mensaje.
- Intervalo de muestreo de métricas.
- Cómo se representa una métrica no disponible (por ejemplo, la temperatura).
