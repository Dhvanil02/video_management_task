from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Specify length for VARCHAR
    path = Column(String(255), nullable=False)  # Specify length for VARCHAR
    size = Column(Integer)  # You can also specify a length if needed
    blocked = Column(Boolean, default=False)  # Blocked field

    def __repr__(self):
        return f"<Video(id={self.id}, name={self.name}, path={self.path}, size={self.size}, blocked={self.blocked})>"
