from fastapi import FastAPI
from routes import router
from db import init_db

# Initialize database
init_db()

app = FastAPI(title="Notification Service")
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Notification Service is running"}