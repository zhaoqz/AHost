from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AppCreate(BaseModel):
    name: str
    description: Optional[str] = None
    slug: Optional[str] = None

class AppResponse(BaseModel):
    id: int
    slug: str
    name: str
    description: Optional[str]
    created_at: datetime
    view_count: int
