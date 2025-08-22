
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, select

# ---------------------
# Database Setup
# ---------------------
DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/loan"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# ---------------------
# SQLAlchemy Model
# ---------------------
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    room_number = Column(Integer)
    address = Column(String(255))
    email = Column(String(100), unique=True)

# ---------------------
# Pydantic Schema
# ---------------------
class PatientCreate(BaseModel):
    name: str
    room_number: Optional[int] = None
    address: Optional[str] = None
    email: str

class PatientRead(PatientCreate):
    id: int

    class Config:
        orm_mode = True

# ---------------------
# FastAPI App
# ---------------------
app = FastAPI()

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

# ---------------------
# API Endpoints
# ---------------------

@app.post("/patients/", response_model=PatientRead)
async def create_patient(patient: PatientCreate, db: AsyncSession = Depends(get_db)):
    new_patient = Patient(**patient.dict())
    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)
    return new_patient

# Cursor-based (scroll) patient retrieval
@app.get("/patients/scroll/", response_model=List[PatientRead])
async def list_patients_scroll(
    after_id: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    query = select(Patient).where(Patient.id > after_id).order_by(Patient.id).limit(limit)
    result = await db.execute(query)
    patients = result.scalars().all()
    return patients



@app.get("/patients/", response_model=List[PatientRead])
async def list_patients(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient))
    patients = result.scalars().all()
    return patients

@app.get("/patients/{patient_id}", response_model=PatientRead)
async def get_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    await db.delete(patient)
    await db.commit()
    return {"message": "Patient deleted successfully"}
