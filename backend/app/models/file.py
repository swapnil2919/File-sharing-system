import uuid
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_filename = Column(String, nullable=False)
    stored_filename = Column(String, nullable=False)
    file_size = Column(BigInteger)
    file_type = Column(String)
    file_path = Column(String)
    file_hash = Column(String, unique=True, index=True)
    max_downloads = Column(Integer, nullable=True)
    download_count = Column(Integer, default=0)
    expires_at = Column(TIMESTAMP, nullable=True)
    is_one_time = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    deleted_at = Column(TIMESTAMP, nullable=True)