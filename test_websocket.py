"""
Prueba simple del WebSocket, para correrlo hay quye tener el servidor uvicorn corriendo
ya despues se ejecuta con: python test_websocket.py (En otra terminal diferente)

"""
import asyncio
import websockets

async def probar_websocket():
    uri = "ws://127.0.0.1:8000/ws"
    
    print("Conectando al WebSocket...")
    async with websockets.connect(uri) as ws:
        print("Conectado exitosamente!")
        
        mensaje = "Hola desde la prueba de WebSocket"
        print(f"Enviando: '{mensaje}'")
        await ws.send(mensaje)
        
        respuesta = await ws.recv()
        print(f"Respuesta recibida: '{respuesta}'")
        
        print("Prueba completada exitosamente!")

asyncio.run(probar_websocket())
