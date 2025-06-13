# core/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from core.router import CommandRouter
from core.manager import AutomatonManager
import uvicorn

app = FastAPI()
manager = AutomatonManager()
router = CommandRouter(manager)

@app.on_event("startup")
def startup_event():
    manager.load_all()

@app.get("/", response_class=HTMLResponse)
async def index():
    # Página simples para testar
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Jarvis Automata UI</title>
    </head>
    <body>
        <h1>Jarvis Automata MVP</h1>
        <button onclick="fetch('/automatons').then(r=>r.json()).then(data=>alert(JSON.stringify(data)))">Listar Autômatos</button>
    </body>
    </html>
    """

@app.get("/automatons")
def list_automatons():
    return manager.list_configs()

@app.post("/register")
def register_automaton(config: dict):
    try:
        automaton_id = manager.register(config)
        return {"automatonId": automaton_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/automatons/{automaton_id}")
def delete_automaton(automaton_id: str):
    try:
        manager.unregister(automaton_id)
        return {}, 204
    except KeyError:
        raise HTTPException(status_code=404, detail="Automaton not found")

@app.post("/run")
def run_automaton(payload: dict):
    try:
        task_id = router.route_run(payload)
        return {"taskId": task_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/status")
def get_status(taskId: str):
    status = router.route_status(taskId)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return status

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)