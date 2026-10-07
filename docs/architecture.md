# Arquitectura

Notas de trabajo. Lo marcado como **abierto** aún no está decidido.

## Componentes

- **Servicio Python** (`service/`): muestrea métricas del sistema en un hilo en segundo
  plano, las expone a los clientes y acepta comandos (terminar un proceso, lanzar un script).
- **Interfaz de escritorio Kotlin** (`desktop/`, aún sin crear): pinta las métricas y envía comandos.

## Decisiones

| Tema | Estado | Notas |
| --- | --- | --- |
| Librería de métricas | Decidido | `psutil` |
| Gestión de dependencias de Python | Decidido | `venv` en `service/.venv` + `requirements.txt` |
| Transporte entre servicio e interfaz | **Abierto** | WebSockets o gRPC |
| Formato de mensaje | **Abierto** | JSON es el candidato probable |
| Intervalo de muestreo | **Abierto** | Entre 500 ms y 1 s |

## Restricciones

- Los sensores de temperatura no existen en todos los sistemas (`psutil` no devuelve nada
  en Windows ni en la mayoría de máquinas virtuales), así que el servicio debe funcionar
  sin esa métrica.
- El proyecto se desarrolla en Pop!_OS y en Windows, por lo que no deben asumirse rutas
  ni comandos de activación exclusivos de Linux.
