from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime


class OwnerBase(BaseModel):
    name: str


class OwnerCreate(OwnerBase):
    pass


class AppointmentBase(BaseModel):
    date_time: datetime.datetime
    description: str


class AppointmentCreate(AppointmentBase):
    pet_id: int


class Appointment(AppointmentBase):
    id: int
    pet_id: int

    model_config = ConfigDict(from_attributes=True)


class PetBase(BaseModel):
    name: str
    species: str


class PetCreate(PetBase):
    pass


class Pet(PetBase):
    id: int
    owner_id: int
    appointments: List[Appointment] = []

    model_config = ConfigDict(from_attributes=True)


class Owner(OwnerBase):
    id: int
    pets: List[Pet] = []

    model_config = ConfigDict(from_attributes=True)
