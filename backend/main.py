from fastapi import FastAPI

# This creates your web server app
app = FastAPI()

# This tells the server what to do when someone visits the main page
@app.get("/")
def read_root():
    return {"message": "Welcome to CodeArena Backend API!"}