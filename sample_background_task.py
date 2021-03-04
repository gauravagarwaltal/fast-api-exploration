import smtplib
import ssl
import time

from fastapi import APIRouter
from fastapi import BackgroundTasks

from models import EmailSchema

back_ground_task_router = APIRouter()


def do_background_task_processing(count: int):
    for _ in range(0, count):
        time.sleep(1)
        print("hello from back-ground-tasks", time.time())


@back_ground_task_router.get("/background-task")
def do_background_processing(email: EmailSchema, background_tasks: BackgroundTasks):
    background_tasks.add_task(do_background_email_processing, email)
    return {"message": "background-task called"}


def do_background_email_processing(email: EmailSchema):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    message = "Message_you_need_to_send"
    try:
        smtp_obj = smtplib.SMTP(smtp_server, port)
        smtp_obj.starttls()
        smtp_obj.login(email.sender, email.password)
        smtp_obj.sendmail(email.sender, email.receivers, message)
        smtp_obj.quit()
        print("email sent!!")
    except Exception as e:
        print("Error: unable to send email", e)
