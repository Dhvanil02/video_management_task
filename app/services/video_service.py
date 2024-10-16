import os
from moviepy.editor import VideoFileClip
from sqlalchemy.orm import Session
from app.models.video import Video
from app.core.database import SessionLocal
from fastapi import HTTPException

class VideoService:

    @staticmethod
    async def convert_to_mp4(video_path: str):
        """Converts a video file to .mp4 format if it's not already .mp4."""
        if not video_path.endswith(".mp4"):
            clip = VideoFileClip(video_path)
            new_path = video_path.rsplit('.', 1)[0] + '.mp4'
            clip.write_videofile(new_path)
            os.remove(video_path)
            return new_path
        return video_path

    @staticmethod
    async def save_video_meta(filename: str, path: str):
        """Saves video metadata to the database, including the size."""
        db: Session = SessionLocal()

        # Get the size of the video file
        size = os.path.getsize(path)  # Size in bytes

        # Create a new Video object, including the size
        video = Video(name=filename, path=path, size=size)

        try:
            # Add and commit the new video to the database
            db.add(video)
            db.commit()
            db.refresh(video)  # Refresh to get the auto-generated ID

        except Exception as e:
            db.rollback()  # Rollback in case of error
            raise e
        finally:
            db.close()  # Close the session

        return video

    @staticmethod
    async def search_videos(name=None, size=None):
        """Searches for videos by name or size."""
        db: Session = SessionLocal()

        try:
            query = db.query(Video)
            
            # Filter by name if provided
            if name:
                query = query.filter(Video.name.contains(name))
            
            # Filter by size if provided (assuming size is a column in Video model)
            if size:
                query = query.filter(Video.size == size)
            
            # Return all matched videos
            return query.all()
        
        finally:
            db.close()  # Close the session

    @staticmethod
    async def is_blocked(video_id: str):
        """Checks if a video is blocked from being accessed."""
        db: Session = SessionLocal()

        try:
            # Fetch video by ID
            video = db.query(Video).filter(Video.id == video_id).first()

            # If video is found, return the blocked status
            if video:
                return video.blocked

            # If video is not found, raise an exception or return False
            raise ValueError(f"Video with ID {video_id} not found.")

        finally:
            db.close()

    @staticmethod
    async def get_video(video_id: str):
        """Fetches a video by its ID."""
        db: Session = SessionLocal()

        try:
            # Fetch video by ID
            video = db.query(Video).filter(Video.id == video_id).first()
            return video
        
        finally:
            db.close()  # Close the session

    @staticmethod
    async def set_block_status(video_id: str, block: bool):
        """Updates the blocked status of a video."""
        db: Session = SessionLocal()

        try:
            # Fetch video by ID
            video = db.query(Video).filter(Video.id == video_id).first()

            if not video:
                raise HTTPException(status_code=404, detail="Video not found")

            # Update the blocked status
            video.blocked = block
            db.commit()
            db.refresh(video)  # Refresh to get the updated values

            return video

        except Exception as e:
            db.rollback()
            raise e

        finally:
            db.close()
