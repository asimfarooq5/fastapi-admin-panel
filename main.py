from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    name: str
    email: str
    password: str


class Todo(BaseModel):
    title: str
    description: str


class Task(BaseModel):
    title: str
    description: str
    todos: List[Todo] = []
    user_id: int = None


users = []
tasks = []


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/users")
async def list_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.post("/users")
async def create_user(user: User):
    users.append(user)
    return RedirectResponse("/users")


@app.get("/tasks")
async def list_tasks(request: Request):
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})


@app.post("/tasks")
async def create_task(task: Task):
    tasks.append(task)
    return RedirectResponse("/tasks")


@app.get("/tasks/{task_id}")
async def get_task(request: Request, task_id: int):
    return templates.TemplateResponse("tasks.html", {"request": request, "task": tasks[task_id - 1]})


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    tasks[task_id - 1] = task
    return {"message": "Task updated successfully!"}


@app.post("/tasks/{task_id}/todos")
async def create_todo_for_task(task_id: int, todo: Todo):
    tasks[task_id - 1].todos.append(todo)
    return {"message": "Todo created successfully!"}


@app.get("/users/{user_id}/tasks")
async def list_tasks_for_user(request: Request, user_id: int):
    tasks_for_user = [task for task in tasks if task.user_id == user_id]
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks_for_user})
