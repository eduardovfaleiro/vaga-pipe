from sqlalchemy.orm import Session
import models

def create_job(db: Session, job_data: dict) -> tuple:
    existing_job = db.query(models.Job).filter(models.Job.url == job_data["url"]).first()
    if existing_job:
        return existing_job, False

    db_job = models.Job(**job_data)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job, True

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()
