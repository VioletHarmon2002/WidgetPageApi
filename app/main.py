from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from app.db import get_conn, create_schema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
) 

create_schema()

@app.get("/")
def default_endpoint():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT version()")
        return cur.fetchone()

@app.get("/users")
def get_users():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM todo_users")
        return cur.fetchall()

class UserCreate(BaseModel):
    username: str

#post a new user to the database
@app.post("/users")
def create_user(user: UserCreate):
    with get_conn() as conn, conn.cursor() as cur:
        
        cur.execute("INSERT INTO todo_users (username) VALUES (%s) RETURNING *", (user.username,))
        return cur.fetchone()

# GET /users/{user_id}
def get_current_user(x_api_key: str = Header(...)):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM todo_users WHERE api_key = %s", (x_api_key,))
        user = cur.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or missing API key")
        return user

# GET /todos for a specific user
@app.get("/todos")
def get_todos(user: dict = Depends(get_current_user)):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT t.id, t.title, t.done, t.created_at, t.updated_at,
                   c.id as category_id, c.category_name
            FROM todo_tasks t
            LEFT JOIN todo_lists c ON t.category_id = c.id
            WHERE t.user_id = %s
        """, (user["id"],))
        return cur.fetchall()

class TodoCreate(BaseModel):
    title: str
    category_id: int

@app.post("/todos")

# POST /todos for a specific user
def create_todo(body: TodoCreate, user: dict = Depends(get_current_user)):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO todo_tasks (user_id, category_id, title)
            VALUES (%s, %s, %s) RETURNING *
        """, (user["id"], body.category_id, body.title))
        return cur.fetchone()

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[str] = None  # timestamp string or None

# update a specific todo for a specific user
@app.put("/todos/{id}")
def update_todo(id: int, body: TodoUpdate, user: dict = Depends(get_current_user)):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            UPDATE todo_tasks SET title = %s, done = %s, updated_at = now()
            WHERE id = %s AND user_id = %s RETURNING *
        """, (body.title, body.done, id, user["id"]))
        task = cur.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return task
# DELETE /todos/{id} for a specific user
@app.delete("/todos/{id}")
def delete_todo(id: int, user: dict = Depends(get_current_user)):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            DELETE FROM todo_tasks WHERE id = %s AND user_id = %s RETURNING *
        """, (id, user["id"]))
        task = cur.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {"deleted": task}


# GET /users/{user_id}/tasks
@app.get("/users/{user_id}/tasks")
def get_user_tasks(user_id: int, user: dict = Depends(get_current_user)):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM todo_tasks WHERE user_id = %s", (user_id,))
        tasks = cur.fetchall()
        if not tasks:
            raise HTTPException(status_code=404, detail="No tasks found for this user")
        return tasks

# GET /categories needed for the frontend dropdown
@app.get("/categories")
def get_categories(user: dict = Depends(get_current_user)):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM todo_lists")
        return cur.fetchall()        