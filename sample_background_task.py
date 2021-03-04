import smtplib
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
    mail_password = email.password,
    sender = email.sender,
    receivers = email.receivers

    message = "Message_you_need_to_send"

    try:
        smtp_obj = smtplib.SMTP('smtp.gmail.com', 2525)
        smtp_obj.starttls()
        smtp_obj.login(sender, mail_password)
        smtp_obj.sendmail(sender, receivers, message)
        smtp_obj.quit()
    except Exception as e:
        print("Error: unable to send email", e)
