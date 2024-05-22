import json
from pathlib import Path
import time
from fastapi import APIRouter, Depends, HTTPException,status
from celery import shared_task, Celery
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from celery.schedules import crontab
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from src.calendarData.models import Event
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig 
from starlette.background import BackgroundTasks

from fastapi.encoders import jsonable_encoder
from asgiref.sync import async_to_sync
# from config import settings
import asyncio

load_dotenv()


router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
)
# celery = Celery('tasks',backend='rpc://',
#                 broker='')


# base_dir = Path(__file__)
# print(base_dir)

# env_path = os.path.join(base_dir, '.env')


# load_dotenv(dotenv_path=env_path)
Mail_Server = os.environ.get("MAIL_SERVER")
conf = ConnectionConfig(
    MAIL_USERNAME="piyush.ratna.64@gmail.com",
    MAIL_PASSWORD="geox xzyb ouiu pkvt",
    MAIL_FROM="piyush.ratna.64@gmail.com",
    MAIL_PORT=465,
    MAIL_SERVER=Mail_Server,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


celery = Celery('tasks', backend='rpc://',
                broker=os.environ.get("CELERY_BROKER_URL"))

celery.conf.timezone = 'UTC'

# @celery.task
# def add(x, y):
#     print(x,y)
#     return x + y


# @celery.task
# def databaseResults():
#     result = asyncio.run(montiorDatabase())
#     json_result = json.dumps(result)
#     return json_result


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, montiorDatabase.s(BackgroundTasks), name='add every 30')

@celery.task
def montiorDatabase():
    # batch=db.query(SmsBatch).all()
    db = SessionLocal()
    current_time = datetime.now()
    data=db.query(Event).filter(Event.updated_at<current_time,Event.notification==False).all()
    print(data)
    if len(data)>0:
        for i in data:
            try:
                message = MessageSchema(
                    subject="Event Starte",
                    recipients=['piyush.ratna.64@gmail.com'],
                    body=f"<p>{i.title} has started'",
                    subtype=MessageType.html
                )
                fm = FastMail(conf)
                background_tasks = BackgroundTasks()
                background_tasks.add_task(fm.send_message, message)
                i.notification=True
                db.commit()
                # await fm.send_message(message)

            except HTTPException as e:
                raise e
            except Exception as e:
                raise e
            

    # db.commit()
    return {}