from fastapi import FastAPI, WebSocket
from simulation import run_simulation_loop

app = FastAPI()

@app.websocket("/ws/simulation")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await run_simulation_loop(websocket)