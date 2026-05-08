import os, psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)

def create_schema():
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
                CREATE EXTENSION IF NOT EXISTS pgcrypto;

                CREATE TABLE IF NOT EXISTS todo_users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR NOT NULL,
                    api_key UUID NOT NULL UNIQUE DEFAULT gen_random_uuid()
                );

                

                

                CREATE TABLE IF NOT EXISTS todo_lists (
                    id SERIAL PRIMARY KEY,
                    category_name VARCHAR NOT NULL
                );

                CREATE TABLE IF NOT EXISTS todo_tasks (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES todo_users(id),
                    category_id INTEGER REFERENCES todo_lists(id),
                    title VARCHAR NOT NULL,
                    done TIMESTAMP,
                    created_at TIMESTAMP DEFAULT now(),
                    updated_at TIMESTAMP DEFAULT now()
                );
            """)
            print("Schema created successfully")

    except Exception as e:
        print(f"Error while creating schema: {e}")
