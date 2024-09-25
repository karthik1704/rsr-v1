import os
from typing import Annotated, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import get_current_user

from ..database import get_async_db
from ..models.resume import (
    DrivingLicense,
    Education,
    Experience,
    LanguageSkill,
    Others,
    Resume,
    TrainingAward,
)
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
    already_resume_exists = await Resume.get_one(db, where_conditions=[Resume.user_id==current_user['id'] ])
    print(already_resume_exists)
    if already_resume_exists is not None:
        raise HTTPException(status_code=402, detail="Resume already Exists, 1 Resume per User can't create more")

    return await Resume.create(db, **resume.model_dump(), user_id=current_user['id'])

@router.put("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_resume(resume_id: int,resume: schemas.ResumeUpdate, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user['id']])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    await db_resume.update(db, **resume.model_dump())

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


@router.put("/{resume_id}/language-skills/", response_model=schemas.Resume)
async def update_resume_language_skill(resume_id: int, language_skill: schemas.LanguageSkillUpdate, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    if language_skill.id is None:
        # Create new language skill
        new_language_skill = LanguageSkill(**language_skill.model_dump(exclude={'id'}), resume_id=resume_id)
        db.add(new_language_skill) 

    else:
        # Update existing language skill
        for existing_language_skill in db_resume.language_skills:
            if existing_language_skill.id == language_skill.id:
                for key, value in language_skill.model_dump(exclude_unset=True).items():
                    setattr(existing_language_skill, key, value)
                break
        else:
            raise HTTPException(status_code=404, detail="Language skill not found")
    
    await db.commit()
    await db.refresh(db_resume)
    return db_resume

@router.delete("/{resume_id}/language-skills/{language_skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume_language_skill(resume_id: int, language_skill_id: int, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    for language_skill in db_resume.language_skills:
        if language_skill.id == language_skill_id:
            await language_skill.delete(db)
            break
    else:
        raise HTTPException(status_code=404, detail="Language skill not found")


@router.put("/{resume_id}/driving-license/", response_model=schemas.Resume)
async def update_resume_driving_license(resume_id: int, driving_license: schemas.DrivingLicenseUpdate, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if driving_license.id is None:
        # Create new driving license
        new_driving_license = DrivingLicense(**driving_license.model_dump(exclude={'id'}), resume_id=resume_id)
        db.add(new_driving_license) 

    else:
        # Update existing driving license
        for existing_driving_license in db_resume.driving_license:
            if existing_driving_license.id == driving_license.id:
                for key, value in driving_license.model_dump(exclude_unset=True).items():
                    setattr(existing_driving_license, key, value)
                break
        else:
            raise HTTPException(status_code=404, detail="Driving license not found")
    
    await db.commit()
    await db.refresh(db_resume)
    return db_resume

@router.delete("/{resume_id}/driving-license/{driving_license_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume_driving_license(resume_id: int, driving_license_id: int, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    for driving_license in db_resume.driving_license:
        if driving_license.id == driving_license_id:
            await driving_license.delete(db)
            break
    else:
        raise HTTPException(status_code=404, detail="Driving license not found")


@router.put("/{resume_id}/training-award/", response_model=schemas.Resume)
async def update_resume_training_award(resume_id: int, training_award: schemas.TrainingAwardUpdate, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])

    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    if training_award.id is None:
        # Create new training award
        new_training_award = TrainingAward(**training_award.model_dump(exclude={'id'}), resume_id=resume_id)
        db.add(new_training_award) 

    else:
        # Update existing training award
        for existing_training_award in db_resume.training_awards:
            if existing_training_award.id == training_award.id:
                for key, value in training_award.model_dump(exclude_unset=True).items():
                    setattr(existing_training_award, key, value)
                break
        else:
            raise HTTPException(status_code=404, detail="Training award not found")
    
    await db.commit()
    await db.refresh(db_resume)
    return db_resume

@router.delete("/{resume_id}/training-award/{training_award_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume_training_award(resume_id: int, training_award_id: int, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    for training_award in db_resume.training_awards:
        if training_award.id == training_award_id:
            await training_award.delete(db)
            break
    else:
        raise HTTPException(status_code=404, detail="Training award not found")


@router.put("/{resume_id}/others/", response_model=schemas.Resume)
async def update_resume_others(resume_id: int,  others: schemas.OthersUpdate, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if others.id is None:
        # Create new training award
        new_others = Others(**others.model_dump(exclude={'id'}), resume_id=resume_id)
        db.add(new_others) 
    
    else: 
        for existing_others in db_resume.others:
            if existing_others.id == others.id:
                for key, value in others.model_dump(exclude_unset=True).items():
                    setattr(existing_others, key, value)
                break
        else:
            raise HTTPException(status_code=404, detail="Others not found")
    
    await db.commit()
    await db.refresh(db_resume)
    return db_resume

@router.delete("/{resume_id}/others/{others_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume_others(resume_id: int, others_id: int, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    for others in db_resume.others:
        if others.id == others_id:
            await others.delete(db)
            break
    else:
        raise HTTPException(status_code=404, detail="Others not found")




@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(resume_id: int, db: db_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    await db_resume.delete(db)
    

UPLOAD_DIRECTORY = "uploads"  # Directory to save uploaded images

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/upload-image/{resume_id}")
async def upload_image(resume_id: int,  db: db_dep, current_user: current_user_dep, file: UploadFile = File(...),):
    # Check if the file is an image
 
    if file.content_type is None or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File type not supported.")

    # Fetch the resume
    resume = await Resume.get_one(db, [Resume.id == resume_id])
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")

    # Delete the existing image if it exists
    if resume.resume_image:
        existing_image_path = resume.resume_image
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)  # Delete the existing image
    # Save the new file
    if file.filename is not None:
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        print(file_location)
        with open(file_location, "wb") as f:
            f.write(await file.read())

    # Update the resume with the new image path
    print(file_location)
    resume.resume_image = os.path.normpath(file_location)  # Save the new image path in the resume
    await db.commit()
    await db.refresh(resume)

    return {"message": "Image uploaded successfully", "resume_image": resume.resume_image}


