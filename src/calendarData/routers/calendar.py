import datetime
from fastapi import APIRouter,Depends, HTTPException
import holidayapi
from src.calendarData import models, schemas
from sqlalchemy import desc
router = APIRouter(
    prefix='/calendarData',
    tags=['calendarData'],
)
from src.database import get_db
from sqlalchemy.orm import Session
import dateutil.parser as dt

@router.get('/getDateEvents/{date}',response_model=list[schemas.Event])
def getDateEvents(date:str,db: Session=Depends(get_db)):
    modified=date
    data=db.query(models.Event).filter(models.Event.event_date==str(modified)).order_by(desc(models.Event.created_at)).all()
    return data



@router.post('/createEvent',response_model=schemas.EventCreated)
def create_event( event: schemas.EventCreate,db: Session=Depends(get_db)):
    db_event = models.Event(
        title=event.title,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time,
        event_date=event.event_date
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    for participant in event.participants:
        db_participant = models.Participant(name=participant.name,event_id=db_event.id)
        db.add(db_participant)
        db.commit()
        db.refresh(db_participant)
    db.commit()
    # stringedDate=str(date_time_obj)[:10:]
    data=db.query(models.Event).filter(models.Event.event_date==str(event.event_date)).order_by(desc(models.Event.created_at)).all()
    # print(data)
    return {'message':f'Event Created for the date {event.event_date}','event':data}



@router.put('/updateEvent/{event_id}', response_model=schemas.EventCreated)
def update_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db_event.title = event.title
    db_event.description = event.description
    db_event.start_time = event.start_time
    db_event.end_time = event.end_time
    db_event.event_date = event.event_date
    
    # Update participants
    for participant in event.participants:
        db_participant = models.Participant(name=participant.name, event_id=event_id)
        db.add(db_participant)
    
    db.commit()
    db.refresh(db_event)
    
    updated_event=db.query(models.Event).filter(models.Event.event_date==str(event.event_date)).order_by(desc(models.Event.created_at)).all()
    # print(data)
    return {'message': 'Event Updated', 'event': updated_event}

@router.delete('/deleteEvent/{event_id}/{date}', response_model=schemas.EventCreated)
def delete_event(event_id: int,date:str, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Delete participants associated with the event
    db.query(models.Participant).filter(models.Participant.event_id == event_id).delete()
    
    # Delete the event
    db.delete(db_event)
    db.commit()
    updated_event=db.query(models.Event).filter(models.Event.event_date==date).order_by(desc(models.Event.created_at)).all()
    return {'message': 'Event Deleted', 'event': updated_event}