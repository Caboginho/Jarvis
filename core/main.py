from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routes import router as products_router
from router import CommandRouter
from manager import AutomatonManager
import uvicorn

app = FastAPI()
manager = AutomatonManager()
router = CommandRouter(manager)

app.mount('/static', StaticFiles(directory='static'), name='static')

@app.on_event("startup")
def startup_event():
    manager.load_all()

@app.get("/", response_class=HTMLResponse)
async def index():
    with open('static/index.html') as f:
        return f.read()

@app.get("/automatons")
def list_automatons():
    return manager.list_configs()

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


app.include_router(products_router, prefix="/products", tags=["Products"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)