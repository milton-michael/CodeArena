from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.database import get_db_connection
import subprocess
import sys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Added problem_id so the backend knows which test case to fetch
class CodeRequest(BaseModel):
    code: str
    problem_id: int

@app.get("/")
def read_root():
    return {"message": "Welcome to CodeArena Backend API!"}

@app.get("/problems")
def get_all_problems():
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    try:
        cursor = conn.cursor(dictionary=True)
        # We only send the problem details to the frontend, NOT the hidden test cases
        cursor.execute("SELECT id, title, description, difficulty FROM problems")
        problems_list = cursor.fetchall()
        return {"problems": problems_list}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

@app.post("/run")
def run_code(request: CodeRequest):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
        
    try:
        cursor = conn.cursor(dictionary=True)
        # Fetch the specific test case for the problem the user is solving
        cursor.execute("SELECT test_case FROM problems WHERE id = %s", (request.problem_id,))
        problem = cursor.fetchone()
        
        if not problem:
            return {"error": "Problem not found in database."}

        # Dynamically attach the database test case to the user's code
        test_script = request.code + problem['test_case']
        
        result = subprocess.run(
            [sys.executable, "-c", test_script],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=5
        )
        
        if result.returncode == 0:
            return {"output": result.stdout}
        else:
            return {"error": result.stderr or result.stdout}
            
    except subprocess.TimeoutExpired:
        return {"error": "Timeout: Your code took too long to execute (Infinite loop?)."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()