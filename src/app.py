from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

# Dependency to get the database session


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Owner Endpoints


@app.post("/owners/", response_model=schemas.Owner)
def create_owner(owner: schemas.OwnerCreate, db: Session = Depends(get_db)):
    db_owner = models.Owner(name=owner.name)
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner


@app.get("/owners/", response_model=List[schemas.Owner])
def read_owners(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    owners = db.query(models.Owner).offset(skip).limit(limit).all()
    return owners


@app.get("/owners/{owner_id}", response_model=schemas.Owner)
def read_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner

# Pet Endpoints


@app.post("/owners/{owner_id}/pets/", response_model=schemas.Pet)
def create_pet_for_owner(
    owner_id: int, pet: schemas.PetCreate, db: Session = Depends(get_db)
):
    db_pet = models.Pet(**pet.model_dump(), owner_id=owner_id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


@app.get("/pets/", response_model=List[schemas.Pet])
def read_pets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pets = db.query(models.Pet).offset(skip).limit(limit).all()
    return pets


@app.get("/pets/{pet_id}", response_model=schemas.Pet)
def read_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

# Appointment Endpoints


@app.post("/pets/{pet_id}/appointments/", response_model=schemas.Appointment)
def create_appointment_for_pet(
    pet_id: int, appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)
):
    db_appointment = models.Appointment(
        **appointment.model_dump(), pet_id=pet_id)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@app.get("/appointments/", response_model=List[schemas.Appointment])
def read_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = db.query(models.Appointment).offset(skip).limit(limit).all()
    return appointments


@app.get("/appointments/{appointment_id}", response_model=schemas.Appointment)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id).first()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
