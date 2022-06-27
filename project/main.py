from celery.result import AsyncResult
from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse

from worker import create_task


app = FastAPI()


@app.get("/")
def home():
    return "app works"


@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    print("entered task")
    filename = payload["filename"]
    task = create_task.delay(filename)
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
        "task_state": task_result.state
    }
    return JSONResponse(result)
