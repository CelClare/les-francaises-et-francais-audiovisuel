from fastapi import FastAPI
from app.api.routes import router
from app.api.test_routes import router as test_router
from app.api.gender_routes import router as gender_router

app = FastAPI(
    title="Les Françaises et les Français dans l'audiovisuel",
    version="0.1"
)

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(router, prefix="/api/v1", tags=["core"])
app.include_router(test_router, prefix="/api/v1", tags=["test"])
app.include_router(gender_router, prefix="/api/v1", tags=["gender"])