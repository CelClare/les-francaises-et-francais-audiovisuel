from fastapi import FastAPI
from app.api.roads import router

app = FastAPI(
    title="Les Françaises et les Français dans l'audiovisuel",
    version="0.1"
)

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(router, prefix="/api/v1")