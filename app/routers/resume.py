from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import get_current_user

from ..database import get_async_db
from ..models.resume import Education, Experience, Resume
from ..schemas import resume as schemas

router = APIRouter(prefix="/resumes")

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
current_user_dep = Annotated[dict, Depends(get_current_user)]

@router.get("/", response_model=List[schemas.Resume])
async def get_all_resumes(db: db_dep, current_user: current_user_dep):
    return await Resume.get_all(db, where_conditions=[Resume.user_id == current_user.get('id')])

@router.get("/{resume_id}", response_model=schemas.Resume)
async def get_resume(resume_id: int, db: db_dep, current_user: current_user_dep):
    return await Resume.get_one(db, where_conditions=[Resume.id == resume_id, Resume.user_id == current_user.get('id')])

@router.post("/", response_model=schemas.Resume, status_code=status.HTTP_201_CREATED)
async def create_resume(resume: schemas.ResumeCreate, db: db_dep, current_user: current_user_dep):
    return await Resume.create(db, **resume.model_dump(), user_id=current_user['id'])

@router.put("/{resume_id}/experiences", response_model=schemas.Resume)
async def update_resume_experience(resume_id: int, experience: schemas.ExperienceUpdate, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if experience.id is None:
        # Create new experience
        new_experience = Experience(**experience.model_dump(exclude={'id'}), resume_id=resume_id)
        db.add(new_experience)

    else:
        # Update existing experience
        for existing_experience in db_resume.experiences:
            if existing_experience.id == experience.id:
                for key, value in experience.model_dump(exclude_unset=True).items():
                    setattr(existing_experience, key, value)
                break
        else:
            raise HTTPException(status_code=404, detail="Experience not found")
    
    await db.commit()
    await db.refresh(db_resume)
    return db_resume

@router.delete("/{resume_id}/experiences/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume_experience(resume_id: int, experience_id: int, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    for experience in db_resume.experiences:
        if experience.id == experience_id:
            await experience.delete(db)
            break


@router.put("/{resume_id}/education", response_model=schemas.Resume)
async def update_resume_education(resume_id: int, education: schemas.EducationUpdate, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if education.id is None:
        # Create new education
        new_education = Education(**education.model_dump(exclude={'id'}), resume_id=resume_id)
        db.add(new_education) 

    else:
        # Update existing education
        for existing_education in db_resume.education:
            if existing_education.id == education.id:
                for key, value in education.model_dump(exclude_unset=True).items():
                    setattr(existing_education, key, value)
                break
        else:
            raise HTTPException(status_code=404, detail="Education not found")
    
    await db.commit()
    await db.refresh(db_resume)
    return db_resume

@router.delete("/{resume_id}/education/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume_education(resume_id: int, education_id: int, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    for education in db_resume.education:
        if education.id == education_id:
            await education.delete(db)
            break



@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(resume_id: int, db: db_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    await db_resume.delete(db)
    

