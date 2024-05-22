import datetime
from sqlalchemy import Boolean, Column, Date, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
# from src.database import Base



class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    event_date=Column(String)
    notification=Column(Boolean,default=False)
    created_at = Column(DateTime,
                        default=datetime.datetime.now(datetime.UTC))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC), onupdate=datetime.datetime.now(datetime.UTC))
    participants = relationship("Participant", back_populates="event")


class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    event_id=Column(ForeignKey('events.id'))
    event=relationship('Event',back_populates='participants')