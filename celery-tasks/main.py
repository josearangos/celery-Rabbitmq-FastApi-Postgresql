from fastapi import FastAPI, BackgroundTasks
from celery_config import celery_app
from pydantic import EmailStr
from pydantic import BaseModel


app = FastAPI(title="Celery Tasks")



class Email(BaseModel):
    email:EmailStr

@app.post("/send_email")
async def send_email(email:Email):
    task_name = "task.send_email"

    task = celery_app.send_task(task_name,args=[email.email],queue="email_to_send") 
    response = {
        "code":202,
        "msg":"Sending email in background",
        "task_id": task.id
    }
    return response