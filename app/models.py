from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ProjectDB(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    places = relationship("PlaceDB", back_populates="project", cascade="all, delete")

    @property
    def is_completed(self) -> bool:
        if not self.places:
            return False
        return all(place.visited for place in self.places)

class PlaceDB(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    external_id = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    visited = Column(Boolean, default=False)
    project = relationship("ProjectDB", back_populates="places")
