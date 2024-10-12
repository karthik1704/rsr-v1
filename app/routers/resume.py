import logging
import os
import shutil
import uuid
from math import exp
from pathlib import Path
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

# @router.put("/{resume_id}/experiences", response_model=schemas.Resume)
# async def update_resume_experience(resume_id: int, experience: schemas.ExperienceUpdate, db: db_dep, current_user: current_user_dep):
#     db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
#     if db_resume is None:
#         raise HTTPException(status_code=404, detail="Resume not found")
    
#     if experience.id is None:
#         # Create new experience
#         new_experience = Experience(**experience.model_dump(exclude={'id'}), resume_id=resume_id)
#         db.add(new_experience)

#     else:
#         # Update existing experience
#         for existing_experience in db_resume.experiences:
#             if existing_experience.id == experience.id:
#                 for key, value in experience.model_dump(exclude_unset=True).items():
#                     setattr(existing_experience, key, value)
#                 break
#         else:
#             raise HTTPException(status_code=404, detail="Experience not found")
    
#     await db.commit()
#     await db.refresh(db_resume)
#     return db_resume

@router.put("/{resume_id}/experiences/multi/", response_model=schemas.Resume)
async def update_resume_experience_multi(resume_id: int, data: schemas.ExperienceUpdateMulti, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    experiences = data.experiences    
    job_applied_for = data.job_applied_for

    if job_applied_for is not None:
        db_resume.job_applied_for = job_applied_for

    if not experiences:
        await db.commit()
        await db.refresh(db_resume)
        return db_resume
    
    incoming_experience_ids = {experience.id for experience in experiences if experience.id is not None}

    # Delete experiences that are not in the incoming data
    for existing_experience in db_resume.experiences:
        if existing_experience.id not in incoming_experience_ids:
            await existing_experience.delete(db)

    for experience in experiences:
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


# @router.put("/{resume_id}/education", response_model=schemas.Resume)
# async def update_resume_education(resume_id: int, education: schemas.EducationUpdate, db: db_dep, current_user: current_user_dep):
#     db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
#     if db_resume is None:
#         raise HTTPException(status_code=404, detail="Resume not found")
    
#     if education.id is None:
#         # Create new education
#         new_education = Education(**education.model_dump(exclude={'id'}), resume_id=resume_id)
#         db.add(new_education) 

#     else:
#         # Update existing education
#         for existing_education in db_resume.education:
#             if existing_education.id == education.id:
#                 for key, value in education.model_dump(exclude_unset=True).items():
#                     setattr(existing_education, key, value)
#                 break
#         else:
#             raise HTTPException(status_code=404, detail="Education not found")
    
#     await db.commit()
#     await db.refresh(db_resume)
#     return db_resume

@router.put("/{resume_id}/education/multi/", response_model=schemas.Resume)
async def update_resume_education_multi(resume_id: int, data: schemas.EducationUpdateMulti, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    educations = data.educations

    

    if not educations:
        raise HTTPException(status_code=400, detail="No educations provided")
    
    incoming_education_ids = {education.id for education in educations if education.id is not None}

    # Delete educations that are not in the incoming data
    for existing_education in db_resume.education:
        if existing_education.id not in incoming_education_ids:
            await existing_education.delete(db)

    for education in educations:
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

    if db_resume.language_skills is None:
        # Create new language skill
        new_language_skill = LanguageSkill(**language_skill.model_dump(exclude={'id'}), resume_id=resume_id)
        db.add(new_language_skill)
    else:
        db_language_skill = await db.execute(select(LanguageSkill).where(LanguageSkill.id == db_resume.language_skills.id, LanguageSkill.resume_id == resume_id))
        db_language_skill = db_language_skill.scalar_one_or_none()

        if db_language_skill is None:
            raise HTTPException(status_code=404, detail="Language skill not found")

        for key, value in language_skill.model_dump(exclude_unset=True).items():
            setattr(db_language_skill, key, value)

    await db.commit()
    await db.refresh(db_resume)
    return db_resume

@router.delete("/{resume_id}/language-skills/{language_skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume_language_skill(resume_id: int, language_skill_id: int, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id') ])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume skill not found")
    
    language_skill = await LanguageSkill.get_one(db, [LanguageSkill.resume_id == resume_id, LanguageSkill.id == language_skill_id])
    
    if language_skill is None:
        raise HTTPException(status_code=404, detail="Language skill not found")

    await language_skill.delete(db)



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

@router.put("/{resume_id}/driving-license/multi/", response_model=schemas.Resume)
async def update_resume_driving_license_multi(resume_id: int, data: schemas.DrivingLicenseUpdateMulti, db: db_dep, current_user: current_user_dep):
        db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
        if db_resume is None:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        driving_licenses = data.driving_licenses

        if not driving_licenses:
            raise HTTPException(status_code=400, detail="No driving licenses provided")
        
        incoming_driving_license_ids = {driving_license.id for driving_license in driving_licenses if driving_license.id is not None}

        # Delete driving licenses that are not in the incoming data
        for existing_driving_license in db_resume.driving_license:
            if existing_driving_license.id not in incoming_driving_license_ids:
                await existing_driving_license.delete(db)

        for driving_license in driving_licenses:
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

@router.put("/{resume_id}/training-award/multi/", response_model=schemas.Resume)
async def update_resume_training_award_multi(resume_id: int, data: schemas.TrainingAwardUpdateMulti, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    training_awards = data.training_awards

    if not training_awards:
        raise HTTPException(status_code=400, detail="No training awards provided")
    
    incoming_training_award_ids = {training_award.id for training_award in training_awards if training_award.id is not None}

    # Delete training awards that are not in the incoming data
    for existing_training_award in db_resume.training_awards:
        if existing_training_award.id not in incoming_training_award_ids:
            await existing_training_award.delete(db)

    for training_award in training_awards:
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

    if others.sectiontitle is None:
        raise HTTPException(status_code=400, detail="Section title is required")
    
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

logger = logging.getLogger(__name__)

@router.delete("/{resume_id}/others/{others_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume_others(resume_id: int, others_id: int,  current_user: current_user_dep, db: db_dep):
    logger.info(f"Deleting 'others' with ID {others_id} from resume {resume_id} for user {current_user.get('id')}")
    
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        logger.warning(f"Resume with ID {resume_id} not found for user {current_user.get('id')}")
        raise HTTPException(status_code=404, detail="Resume not found")

    for others in db_resume.others:
        if others.id == others_id:
            await others.delete(db)
            logger.info(f"Successfully deleted 'others' with ID {others_id} from resume {resume_id}")
            break
    else:
        logger.warning(f"'Others' with ID {others_id} not found in resume {resume_id}")
        raise HTTPException(status_code=404, detail="Others not found")





@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(resume_id: int, db: db_dep, current_user: current_user_dep):
    db_resume = await Resume.get_one(db, [Resume.id == resume_id, Resume.user_id == current_user.get('id')])
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    await db_resume.delete(db)
    

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-image/{resume_id}/")
async def upload_image(
    resume_id: int, 
    db: db_dep, 
    current_user: current_user_dep, 
    file: UploadFile = File(...),
):
    # Check if the file is an image
    if file.content_type is None or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File type not supported.")

    # Fetch the resume
    resume = await Resume.get_one(db, [Resume.id == resume_id])
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")

    # Delete the existing image if it exists
    if resume.resume_image:
    # Convert the relative URL to an absolute path
        existing_image_path = UPLOAD_DIR / Path(resume.resume_image).name  # Get the filename and append to UPLOAD_DIR
        if existing_image_path.exists():
            try:
                os.remove(existing_image_path)  # Delete the existing image
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to delete existing image: {str(e)}")
    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}-{file.filename}"
    file_location = UPLOAD_DIR / unique_filename

    # Save the new file
    try:
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)  # Save the file efficiently
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save the file: {str(e)}")
    finally:
        await file.close()  # Close the file to free up resources

    # Update the resume with the new image path
    resume.resume_image = f"/static/{unique_filename}" # Save the new image path in the resume
    await db.commit()
    await db.refresh(resume)

    return {"message": "Image uploaded successfully", "resume_image": resume.resume_image}

