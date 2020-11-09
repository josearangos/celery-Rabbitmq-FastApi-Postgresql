from celery_config import celery_app
from celery.utils.log import get_task_logger
from pydantic import EmailStr

import time


logger = get_task_logger(__name__)


@celery_app.task(acks_late=True)
def send_email(email:EmailStr):        
    logger.info("Sending email to %s ..." % (email))
    time.sleep(10)
    logger.info("Email sended")
