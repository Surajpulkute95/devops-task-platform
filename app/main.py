from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="DevOps Task Platform")


class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


class Task(TaskCreate):
    id: int


tasks = []
next_task_id = 1


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/tasks")
def create_task(task: TaskCreate):
    global next_task_id

    new_task = Task(
        id=next_task_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
    )

    tasks.append(new_task)
    next_task_id += 1

    return new_task


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}

    raise HTTPException(status_code=404, detail="Task not found")
