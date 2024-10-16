from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks
from app.services.video_service import VideoService
from app.models.video import Video
import shutil
import os
import shutil

router = APIRouter()

@router.post("/upload/")
async def upload_video(file: UploadFile, background_tasks: BackgroundTasks):
    # Define the folder where videos will be stored
    videos_folder = "videos"
    
    # Check if the 'videos' directory exists; if not, create it
    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder)

    # Validate the file format
    if not file.filename.endswith(('.mp4', '.avi', '.mov')):
        raise HTTPException(status_code=400, detail="Invalid video format")
    
    # Construct the full path for the uploaded video
    video_path = os.path.join(videos_folder, file.filename)
    
    # Save the file locally
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Add background task to convert video to .mp4 if required
    background_tasks.add_task(VideoService.convert_to_mp4, video_path)
    
    # Save video metadata
    video = await VideoService.save_video_meta(file.filename, video_path)
    
    return {"message": "Video uploaded successfully", "video": video}


@router.get("/search")
async def search_video(name: str = None, size: int = None):
    videos = await VideoService.search_videos(name, size)
    if not videos:
        raise HTTPException(status_code=404, detail="No videos found")
    return {"videos": videos}

@router.get("/video/{video_id}")
async def get_video(video_id: str):
    if await VideoService.is_blocked(video_id):
        raise HTTPException(status_code=403, detail="This video is blocked for downloading")
    
    video = await VideoService.get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return {"video": video}

@router.put("/videos/{video_id}/block")
async def block_video(video_id: str, block: bool):
    try:
        # Use the VideoService to set the block status
        video = await VideoService.set_block_status(video_id, block)
        return {
            "message": f"Video {'blocked' if block else 'unblocked'} successfully",
            "video": {
                "id": video.id,
                "name": video.name,
                "blocked": video.blocked
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))