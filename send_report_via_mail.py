from fastapi import APIRouter, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.responses import JSONResponse

from models import EmailSchema

mail_router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME="MAIL_USERNAME",
    MAIL_PASSWORD="MAIL_PASSWORD",
    MAIL_FROM="MAIL_FROM",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=False,
    MAIL_SSL=True,
    USE_CREDENTIALS=True
)

template = """
<p>Thanks for using Fastapi-mail</p> 
"""


@mail_router.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.receivers,  # List of recipients, as many as you can pass
        body=template,
        subtype="html"
    )
    conf.MAIL_USERNAME = email.username
    conf.MAIL_PASSWORD = email.password
    conf.MAIL_FROM = email.sender
    try:
        fm = FastMail(conf)
        await fm.send_message(message)
    except Exception as e:
        raise HTTPException(detail=e, status_code=400)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
