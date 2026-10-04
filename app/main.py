from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth,users



def create_application():
    app = FastAPI(
        title = "User Management API",
        description="API for user authentication, management, and background tasks.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(users.router)

    return app

app = create_application()

@app.get("/health", tags=["Health Check"])
def health_check():
    """Health check endpoint to verify server status."""
    return {"status": "healthy", "service": "User-Management"}