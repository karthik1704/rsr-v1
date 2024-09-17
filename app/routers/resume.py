from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_db
from ..models import resume as models
from ..schemas import resume as schemas

router = APIRouter(prefix="/resumes")

db_dep = Annotated[AsyncSession, Depends(get_async_db)]

@router.post("/", response_model=schemas.Resume)
async def create_resume(resume: schemas.ResumeCreate, db: db_dep):
    db_resume = await models.Resume.create(db, **resume.personal_info.model_dump())

    for exp in resume.experiences:
        db_experience = models.Experience(**exp.model_dump(), resume_id=db_resume.id)
        db.add(db_experience)

    for edu in resume.education:
        db_education = models.Education(**edu.model_dump(), resume_id=db_resume.id)
        db.add(db_education)

    await db.commit()
    await db.refresh(db_resume)
    return db_resume

@router.get("/", response_model=List[schemas.Resume])
async def read_resumes( db: db_dep,skip: int = 0, limit: int = 100,):
    resumes = await models.Resume.get_all(db, skip=skip, limit=limit)
    return resumes

@router.get("/{resume_id}", response_model=schemas.Resume)
async def read_resume(resume_id: int, db: db_dep):
    db_resume = await models.Resume.get_one(db, [models.Resume.id == resume_id])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume

@router.put("/{resume_id}", response_model=schemas.Resume)
async def update_resume(resume_id: int, resume: schemas.ResumeUpdate, db: db_dep):
    db_resume = await models.Resume.get_one(db, [models.Resume.id == resume_id])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Update personal info
    await db_resume.update(db, **resume.personal_info.model_dump())

    # Update experiences
    db_resume.experiences = []
    for exp in resume.experiences:
        db_experience = models.Experience(**exp.model_dump(), resume_id=db_resume.id)
        db_resume.experiences.append(db_experience)

    # Update education
    db_resume.education = []
    for edu in resume.education:
        db_education = models.Education(**edu.model_dump(), resume_id=db_resume.id)
        db_resume.education.append(db_education)

    await db.commit()
    await db.refresh(db_resume)
    return db_resume

@router.delete("/{resume_id}", response_model=schemas.Resume)
async def delete_resume(resume_id: int, db: db_dep):
    db_resume = await models.Resume.get_one(db, [models.Resume.id == resume_id])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    await db_resume.delete(db)
    return db_resume