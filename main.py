import time

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import pdb

app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins)

in_memory_database = []


class Request(BaseModel):
    username: str
    password: str
    email: str


class Response(BaseModel):
    username: str
    email: str


class RegisterUserRequest(BaseModel):
    email: str
    phone_number: str
    password: str


class RegisterUserResponse(BaseModel):
    email: Optional[str] = ""
    phone_number: Optional[str] = ""
    message:str


async def is_user_present(phone_number):
    for data in in_memory_database:
        if "phone_number" in data:
            if data["phone_number"] == phone_number:
                return True
    return False


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"request processed in {process_time} s")
    return response


@app.get("/home")
def home():
    return {"Hello": "GET"}


@app.post("/login", response_model=Response)
def home_post(req: Request):
    if req.username == "testdriven.io" and req.password == "testdriven.io":
        return req
    return {"message": "Authentication Failed"}


@app.post("/register/user", response_model=RegisterUserResponse)
async def register_user(req: RegisterUserRequest):
    result = await is_user_present(req.phone_number)
    if result:
        return {
            "message":"user is already present",
            "email":req.email,
            "phone_number":req.phone_number
        }
    data_dict = {}
    data_dict["email"] = req.email
    data_dict["password"] = req.password
    data_dict["phone_number"] = req.phone_number
    in_memory_database.append(data_dict)
    return {"message":"user has been added"}


@app.get("/employee/{employee_id}")
def employee_identity(employee_id: int):
    return {"id": employee_id}


@app.post("/employee")
def employee_department(department: str):
    return {"department": department}


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
