from fastapi import APIRouter

from models import (
    RegisterUserRequest as User,
    DriverLogsRequest as Dlr,
)

memory_router = APIRouter()

USERPROFILE_DOC_TYPE = "userprofile"
RIDE_DOC_TYPE = "userRide"

user_data = dict()
driver_data = dict()


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


async def put_driver_data(dlr: Dlr):
    document = dlr.dict()
    if dlr.phone_number not in driver_data:
        driver_data.update({dlr.phone_number:[document]})
    else:
        driver_data[f"{dlr.phone_number}"].append(document)
    return True


async def get_driver_data(phone_number: str):
    if phone_number not in driver_data:
        return {}
    else:
        return {phone_number: driver_data[phone_number]}
