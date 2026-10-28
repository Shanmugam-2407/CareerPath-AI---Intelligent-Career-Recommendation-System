"""
FastAPI Main Application Entrypoint.
Production-style modular backend exposing ML, NLP, and AI career recommendations.
"""
import sys
from pathlib import Path

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.routes.profile import router as profile_router
from backend.routes.career import router as career_router
from backend.routes.roadmap import router as roadmap_router
from backend.routes.tasks import router as tasks_router
from backend.routes.projects import router as projects_router

app = FastAPI(
    title="AI-Powered Personalized Career Path Generator",
    description="Production-style ML, NLP, and AI-driven career recommendation and roadmap engine.",
    version="1.0.0"
)

# Enable CORS for frontend connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(profile_router)
app.include_router(career_router)
app.include_router(roadmap_router)
app.include_router(tasks_router)
app.include_router(projects_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "InternalServerError", "message": str(exc)}
    )


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "AI-Powered Personalized Career Path Generator",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
