from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ParticipantBase(BaseModel):
    name: str

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    id: int

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    event_date:str

class EventCreate(EventBase):
    participants: List[ParticipantCreate]



class Event(EventBase):
    id: int
    participants: List[Participant]

    class Config:
        orm_mode = True

class EventCreated(BaseModel):
    message:str
    event:List[Event] 