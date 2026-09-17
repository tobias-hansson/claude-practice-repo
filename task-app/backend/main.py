# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your frontend's origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskCreate(BaseModel):
    title: str

class Task(BaseModel):
    id: int
    title: str
    done: bool = False

tasks: list[Task] = []
next_id = 1

@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def add_task(task: TaskCreate):
    global next_id
    new_task = Task(id=next_id, title=task.title, done=False)
    tasks.append(new_task)
    next_id += 1
    return new_task

@app.post("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    for t in tasks:
        if t.id == task_id:
            t.done = True
            return t
    raise HTTPException(status_code=404, detail="Task not found")
