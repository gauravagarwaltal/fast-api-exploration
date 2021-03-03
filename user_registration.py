from fastapi import APIRouter

from couchDB_client import is_user_present, put_user
from models import RegisterUserRequest, RegisterUserResponse

register_user_router = APIRouter()


@register_user_router.post("/users", response_model=RegisterUserResponse)
async def register_user(req: RegisterUserRequest):
    result = await is_user_present(req.phone_number)
    if result:
        return {
            "message": "user is already present",
            "email": req.email,
            "phone_number": req.phone_number
        }
    await put_user(req)
    return {"message": "user has been added"}


@register_user_router.get("/users/{phone_number}", response_model=RegisterUserResponse)
async def register_user(phone_number: str):
    result = await is_user_present(phone_number)
    if result:
        result.update({"message": "user has found"})
        return result
    return {"message": "user has not found"}
