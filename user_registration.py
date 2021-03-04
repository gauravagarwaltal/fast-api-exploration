import os

from fastapi import APIRouter, HTTPException

import memory_client
from couchDB_client import is_user_present, put_user
from models import RegisterUserRequest, RegisterUserResponse

register_user_router = APIRouter()
DB_TYPE = os.environ.get("DB_TYPE", "in-memory")


@register_user_router.post("/users", response_model=RegisterUserResponse)
async def register_new_user(req: RegisterUserRequest):
    if DB_TYPE == "in-memory":
        result = await memory_client.is_user_present(req.phone_number)
    else:
        result = await is_user_present(req.phone_number)
    if result:
        raise HTTPException(detail=RegisterUserResponse(**{
            "message": "user is already present",
            "email": req.email,
            "phone_number": req.phone_number
        }).dict(), status_code=400)
    if DB_TYPE == "in-memory":
        await memory_client.put_user(user=req)
    else:
        await put_user(req)
    return {"message": "user has been added"}


@register_user_router.get("/users/{phone_number}")
async def fetch_user_details(phone_number: str):
    if DB_TYPE == "in-memory":
        result = await memory_client.is_user_present(phone_number)
    else:
        result = await is_user_present(phone_number)
    if result:
        result.update({"message": "user has found"})
        return result
    raise HTTPException(detail=RegisterUserResponse(**{"message": "user has not found"}).dict(), status_code=400)
