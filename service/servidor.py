import asyncio
import json
import websockets.exceptions
from websockets.asyncio.server import serve
from monitor import leer_metricas


async def iniciarLecturaMetricas(websocket):
    try:
        while True:
            # Enviamos las métricas en formato JSON
            await websocket.send(json.dumps(leer_metricas()))
            await asyncio.sleep(0.5)
    except websockets.exceptions.ConnectionClosed:
        print("\nCliente desconectado de forma segura.")

async def main():
    async with serve(iniciarLecturaMetricas, "localhost", 8765):
        await asyncio.Future()   # mantiene el servidor abierto

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario (Ctrl+C).")