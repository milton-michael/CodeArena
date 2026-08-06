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

# This model defines the structure of the incoming data
class CodeRequest(BaseModel):
    code: str

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
        cursor.execute("SELECT * FROM problems")
        problems_list = cursor.fetchall()
        return {"problems": problems_list}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

@app.post("/run")
def run_code(request: CodeRequest):
    try:
        # Run the code safely using the exact Python executable running the server
        result = subprocess.run(
            [sys.executable, "-c", request.code],
            capture_output=True,
            text=True,
            timeout=5 # Kills the code if it takes more than 5 seconds (prevents infinite loops)
        )
        
        if result.returncode == 0:
            return {"output": result.stdout}
        else:
            return {"error": result.stderr}
            
    except subprocess.TimeoutExpired:
        return {"error": "Timeout: Your code took too long to execute (Infinite loop?)."}
    except Exception as e:
        return {"error": str(e)}