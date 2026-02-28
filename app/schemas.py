from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class PlaceBase(BaseModel):
    external_id: int
    notes: Optional[str] = None
    visited: bool = False

class PlaceCreate(PlaceBase):
    pass

class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    visited: Optional[bool] = None

class PlaceResponse(PlaceBase):
    id: int
    project_id: int
    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    places: List[PlaceCreate] = Field(min_length=1, max_length=10)

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    is_completed: bool
    places: List[PlaceResponse]
    class Config:
        from_attributes = True
