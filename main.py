import time

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins)


class Request(BaseModel):
    username: str
    password: str
    email: str


class Response(BaseModel):
    username: str
    email: str


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
