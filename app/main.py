from fastapi import FastAPI
from app.api.video import router as video_router
from app.core.database import Base, engine

# Initialize the FastAPI app
app = FastAPI()

# Include the video router for video-related endpoints
app.include_router(video_router, prefix="/api", tags=["videos"])

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Root endpoint (for testing the API)
@app.get("/")
async def root():   
    return {"message": "Welcome to the FastAPI Video Management System"}
