"""
Global Team Manager Backend - FastAPI Application Entry Point

This is the main entry point for the Global Team Manager backend API.
It provides endpoints for team coordination across different time zones,
including user authentication, team management, meeting scheduling,
and availability tracking.

Architecture:
- FastAPI framework with async/await support
- JSON file-based storage (backend/data/)
- JWT-based authentication
- Modular route organization with controllers and services
- CORS enabled for frontend integration

Import Structure:
- All imports use absolute paths under the backend package
- When running 'python app.py' from the backend directory, sys.path is adjusted
- All modules use direct imports (e.g., 'from controllers.auth_controller import AuthController')
- No relative imports (e.g., 'from ..controllers') are used for compatibility

Main Features:
- User authentication and profile management
- Team creation and member management
- Meeting scheduling with time zone support
- Availability tracking and voting
- Cross-timezone coordination
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path for imports
# All imports use absolute paths under the backend package
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Load environment variables from .env.development
try:
    from dotenv import load_dotenv
    env_path = backend_dir / '.env.development'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded environment variables from {env_path}")
    else:
        print(f"⚠️  No .env.development file found at {env_path}")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import all route modules
from routes import auth, teams, members, meetings, aggregation

# Initialize FastAPI application
app = FastAPI(
    title="Global Team Manager API",
    description="Backend API for coordinating team members across different time zones",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc",  # ReDoc at /redoc
)

# CORS Middleware Configuration
# This allows the frontend (running on different port) to make requests to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("VITE_API_URL")
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Health Check Endpoint
@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint providing basic health check and API information.
    
    Returns:
        dict: API status and basic information
    """
    return {
        "message": "Backend is running",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs",
        "api_base": "/api/v1"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Detailed health check endpoint for monitoring.
    
    Returns:
        dict: Detailed health status including data directory access
    """
    try:
        # Check if data directory is accessible
        data_dir = Path(__file__).parent / "data"
        data_dir.mkdir(exist_ok=True)
        
        return {
            "status": "healthy",
            "data_directory": str(data_dir),
            "data_accessible": data_dir.exists(),
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# Register API Routes
# Each route module is mounted with its specific prefix and tags

# Authentication routes: /api/v1/auth/*
app.include_router(auth.router)

# Teams routes: /api/v1/teams/*
app.include_router(teams.router)

# Members routes: /api/v1/members/*
app.include_router(members.router)

# Meetings routes: /api/v1/meetings/*
app.include_router(meetings.router)

# Aggregation routes: /api/v1/aggregation/*
app.include_router(aggregation.router)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: The incoming request
        exc: The exception that occurred
        
    Returns:
        JSONResponse: Error response with appropriate status code
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG", "false").lower() == "true" else "An unexpected error occurred"
        }
    )

# Application Startup Event
@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    Performs initialization tasks when the application starts.
    """
    print("🚀 Starting Global Team Manager Backend...")
    
    # Ensure data directory exists
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    print(f"📁 Data directory: {data_dir}")
    
    # Check environment configuration
    jwt_secret = os.getenv("JWT_SECRET", "dev-secret")
    if jwt_secret == "dev-secret":
        print("⚠️  Using default JWT secret. Set JWT_SECRET in .env.development for production!")
    
    print("✅ Backend startup complete!")

# Application Shutdown Event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler.
    Performs cleanup tasks when the application shuts down.
    """
    print("🛑 Shutting down Global Team Manager Backend...")
    print("✅ Backend shutdown complete!")

if __name__ == "__main__":
    """
    Direct execution entry point.
    
    Run the backend with: python app.py
    """
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    
    print(f"🌐 Starting server on {host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    
    # Start the server
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if not debug else "debug"
    )
