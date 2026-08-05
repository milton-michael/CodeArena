from fastapi import FastAPI
from backend.database import get_db_connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to CodeArena Backend API!"}

# NEW ROUTE: Fetch all problems from the database
@app.get("/problems")
def get_all_problems():
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM problems")
        problems_list = cursor.fetchall()
        return {"problems": problems_list}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()