from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    email: str
    phone_number: str
    password: str


class RegisterUserResponse(BaseModel):
    email: Optional[str] = ""
    phone_number: Optional[str] = ""
    message: str


class Request(BaseModel):
    username: str
    password: str
    email: str


class Response(BaseModel):
    username: str
    email: str


class DriverLogsRequest(BaseModel):
    start_time: datetime
    end_time: datetime
    distance_travelled: int
    phone_number: str

