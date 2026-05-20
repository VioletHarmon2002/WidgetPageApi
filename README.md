# 📝 ToDo Widget API

A full-stack ToDo application built with **FastAPI**, **PostgreSQL**, **Docker**, and a **vanilla JavaScript frontend widget**. This project includes a backend API, database integration, authentication with API keys, and frontend integration into a customizable start page.

##  Live Demo


### Frontend
 https://people.arcada.fi/~kallioel/startpageGirls/startpage-girls/

### API
 https://todo-girls-git-todo-girls.2.rahtiapp.fi

### API Documentation (Swagger UI)
 https://todo-girls-git-todo-girls.2.rahtiapp.fi/docs

---

##  Repositories

### Frontend Repository
 https://github.com/VioletHarmon2002/WidgetPageFrontEnd

### Backend Repository
 https://github.com/VioletHarmon2002/WidgetPageApi

---

##  Features

###  ToDo Database
- PostgreSQL database running with Docker Compose
- Three connected tables:
  - `todo_users`
  - `todo_lists` (categories)
  - `todo_tasks`
- Proper primary and foreign keys
- Automatic database schema creation
- Automatic category seeding:
  - Work
  - Personal
  - School
  - Shopping
  - Health
  - Sport

###  FastAPI Backend
Implemented CRUD functionality:

#### Todos
- `GET /todos`
- `POST /todos`
- `PUT /todos/{id}`
- `DELETE /todos/{id}`

#### Categories
- `GET /categories`

Features:
- JOIN query for category names
- FastAPI dependency injection
- API key authentication
- CORS configuration for frontend communication

###  Frontend Widget
- Built with **HTML, CSS, Bootstrap, and Vanilla JavaScript**
- Loads tasks automatically on page load
- Dynamic category dropdown
- Mark tasks as completed
- Strikethrough effect for completed tasks
- Delete confirmation popup
- Settings modal for API configuration

###  Authentication
Authentication is handled using API keys.

Each user receives a unique key automatically using:

```sql
gen_random_uuid()
```

The API key is sent in:

```http
X-API-Key
```

Unauthorized access returns:

```http
401 Unauthorized
```

The frontend stores settings in `localStorage`.

###  Deployment
The project is deployed using:

- **Rahti OpenShift** for the FastAPI backend
- **people.arcada.fi** for frontend hosting
- **Docker Compose** for local PostgreSQL development

---

##  Technologies Used

### Backend
- FastAPI
- PostgreSQL
- Docker
- SQL
- Python

### Frontend
- HTML
- CSS
- Bootstrap
- Vanilla JavaScript

### Deployment
- Rahti OpenShift
- people.arcada.fi

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/WidgetPageApi.git
cd WidgetPageApi
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start PostgreSQL with Docker

```bash
docker compose up
```

### 4. Run FastAPI

```bash
uvicorn app.main:app --reload
```

API will run at:

```txt
http://127.0.0.1:8000
```

Swagger docs:

```txt
http://127.0.0.1:8000/docs
```

---

##  Testing the Application

Open the frontend in an incognito/private browser window.

1. Open the start page
2. Click the ⚙️ settings button
3. Enter:

**API URL**
```txt
https://todo-girls-git-todo-girls.2.rahtiapp.fi
```

4. Add your API key
5. Save changes

The ToDo widget will automatically load tasks.

You can:
-  Add tasks
-  Mark tasks as completed
-  Delete tasks

---



## 📄 License

This project was created for educational purposes at Arcada University of Applied Sciences.