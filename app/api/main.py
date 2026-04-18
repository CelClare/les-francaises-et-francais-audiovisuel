from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.api.gender_routes import router as gender_router
from app.api.jt_routes import router as jt_router
from app.api.gender_public_private_routes import router as gender_public_private_router

app = FastAPI(
    title="Les Françaises et les Français dans l'audiovisuel",
    version="0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "API is running"}


app.include_router(router, prefix="/api/v1", tags=["core"])
app.include_router(gender_router, prefix="/api/v1", tags=["gender"])
app.include_router(jt_router, prefix="/api/v1", tags=["jt"])
app.include_router(gender_public_private_router, prefix="/api/v1", tags=["gender-public-private"])