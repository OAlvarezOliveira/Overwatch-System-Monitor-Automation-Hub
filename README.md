# Overwatch System Monitor & Automation Hub

Proyecto de aprendizaje que combina **Python** y **Kotlin**: un servicio en segundo
plano que monitoriza el equipo y ejecuta tareas de automatización, y un panel de
escritorio que muestra todo en tiempo real.

> **Estado:** desarrollo temprano. Todavía no funciona de extremo a extremo.
> Consulta el [diario de progreso](docs/progress/README.md) para ver qué está hecho y qué toca.

## Idea

```
[ Servicio Python ]  <---- protocolo de red local ---->  [ Interfaz de escritorio Kotlin ]
  - hilos: muestreo de CPU / RAM / disco                   - dashboard en tiempo real
  - subprocess / multiprocessing: procesos y scripts       - gestor de procesos
  - control del sistema (listar / terminar procesos)       - consola de automatización y alertas
```

## Objetivos

- Practicar concurrencia real: hilos y `asyncio` en Python, corrutinas en Kotlin.
- Conectar dos ecosistemas de lenguajes mediante un protocolo local (IPC por red).
- Trabajar conceptos de sistemas operativos: procesos, señales y métricas de hardware.

## Estructura del repositorio

| Ruta | Contenido |
| --- | --- |
| `service/` | Servicio de monitorización en Python (aquí viven el entorno virtual y las dependencias) |
| `docs/` | Notas de arquitectura, hoja de ruta y diario de progreso |

La carpeta `desktop/` con la app Kotlin se añadirá cuando empiece esa fase.

## Puesta en marcha (servicio)

Requiere Python 3.12 o superior.

Linux / macOS:

```bash
cd service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
cd service
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si PowerShell bloquea el script de activación, ejecuta una vez
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Documentación

- [Arquitectura](docs/architecture.md)
- [Hoja de ruta](docs/roadmap.md)
- [Overwatch por asignatura](docs/asignaturas.md)
- [Registro de decisiones](docs/decisiones.md)
- [Diario de progreso](docs/progress/README.md)
