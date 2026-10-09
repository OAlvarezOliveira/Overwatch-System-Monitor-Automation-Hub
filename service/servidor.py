# -*- coding: utf-8 -*-
import asyncio
import json
from websockets.asyncio.server import serve
from monitor import leer_metricas

async def iniciarLecturaMetricas(websocket):
    while True:
        await websocket.send(json.dumps(leer_metricas()))
        await asyncio.sleep(0.5)

async def main():
    async with serve(iniciarLecturaMetricas, "localhost", 8765):
        await asyncio.Future()   # mantiene el servidor abierto

asyncio.run(main())