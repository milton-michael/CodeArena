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
        # Append automated test assertions to the user's script
        test_script = request.code + """

# --- AUTOMATED TEST SUITE ---
try:
    result = two_sum([2, 7, 11, 15], 9)
    assert result in ([0, 1], [1, 0], (0, 1), (1, 0)), f"Expected [0, 1], got {result}"
    print("Test Result: ACCEPTED [PASS]")
except Exception as e:
    print(f"Test Result: WRONG ANSWER [FAIL]\\nDetails: {e}")
"""
        
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