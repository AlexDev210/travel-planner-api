from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, get_db
import models
import schemas
import services


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Planner API")


@app.post("/projects/", response_model=schemas.ProjectResponse, status_code=201)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    external_ids = [p.external_id for p in project.places]
    if len(external_ids) != len(set(external_ids)):
        raise HTTPException(status_code=400, detail="Duplicate places in the creation request.")

    for ext_id in external_ids:
        await services.verify_place_exists(ext_id)

    db_project = models.ProjectDB(name=project.name, description=project.description, start_date=project.start_date)
    db.add(db_project)
    db.flush()

    for place in project.places:
        db_place = models.PlaceDB(project_id=db_project.id, external_id=place.external_id, notes=place.notes,
                                  visited=place.visited)
        db.add(db_place)

    db.commit()
    db.refresh(db_project)
    return db_project


@app.get("/projects/", response_model=List[schemas.ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.ProjectDB).all()


@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.ProjectDB).filter(models.ProjectDB.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/projects/{project_id}", response_model=schemas.ProjectResponse)
def update_project(project_id: int, project_update: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(models.ProjectDB).filter(models.ProjectDB.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)
    return db_project


@app.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(models.ProjectDB).filter(models.ProjectDB.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    if any(place.visited for place in db_project.places):
        raise HTTPException(status_code=400, detail="Cannot delete project: one or more places are marked as visited.")

    db.delete(db_project)
    db.commit()
    return None


@app.post("/projects/{project_id}/places/", response_model=schemas.PlaceResponse, status_code=201)
async def add_place_to_project(project_id: int, place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    db_project = db.query(models.ProjectDB).filter(models.ProjectDB.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    if len(db_project.places) >= 10:
        raise HTTPException(status_code=400, detail="Project already has the maximum of 10 places.")
    if any(p.external_id == place.external_id for p in db_project.places):
        raise HTTPException(status_code=400, detail="Place already exists in this project.")

    await services.verify_place_exists(place.external_id)

    db_place = models.PlaceDB(**place.dict(), project_id=project_id)
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


@app.get("/projects/{project_id}/places/", response_model=List[schemas.PlaceResponse])
def list_places(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.PlaceDB).filter(models.PlaceDB.project_id == project_id).all()


@app.get("/projects/{project_id}/places/{place_id}", response_model=schemas.PlaceResponse)
def get_place(project_id: int, place_id: int, db: Session = Depends(get_db)):
    db_place = db.query(models.PlaceDB).filter(models.PlaceDB.project_id == project_id,
                                               models.PlaceDB.id == place_id).first()
    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")
    return db_place


@app.put("/projects/{project_id}/places/{place_id}", response_model=schemas.PlaceResponse)
def update_place(project_id: int, place_id: int, place_update: schemas.PlaceUpdate, db: Session = Depends(get_db)):
    db_place = db.query(models.PlaceDB).filter(models.PlaceDB.project_id == project_id,
                                               models.PlaceDB.id == place_id).first()
    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")

    update_data = place_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_place, key, value)

    db.commit()
    db.refresh(db_place)
    return db_place
