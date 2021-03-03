from fastapi import APIRouter

from models import RegisterUserRequest as User

memory_router = APIRouter()

USERPROFILE_DOC_TYPE = "userprofile"
RIDE_DOC_TYPE = "userRide"

user_data = dict()


async def is_user_present(phone_number: str):
    doc_id = f"{USERPROFILE_DOC_TYPE}::{phone_number}"
    result: dict = user_data.get(doc_id)
    if not result:
        return None
    return result


async def put_user(user: User):
    doc_id = f"userprofile::{user.phone_number}"
    document = user.dict()
    document.update({'_id': doc_id})
    _tuple_object = user_data.update({doc_id: document})
    return True
