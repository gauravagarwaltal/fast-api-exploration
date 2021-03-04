import couchdb
from couchdb import Database, Document
from fastapi import HTTPException

from models import RegisterUserRequest as User, DriverLogsRequest

USERPROFILE_DOC_TYPE = "userprofile"
RIDE_DOC_TYPE = "userRide"


def get_bucket() -> Database:
    couch = couchdb.Server('http://admin:iamthegod@127.0.0.1:5984/')
    db = couch['poc_db']
    return db


async def is_user_present(phone_number: str):
    doc_id = f"{USERPROFILE_DOC_TYPE}::{phone_number}"
    db_instance: Database = get_bucket()
    result: Document = db_instance.get(doc_id, quiet=True)
    if not result:
        return None
    return result


async def put_user(user: User):
    doc_id = f"{USERPROFILE_DOC_TYPE}::{user.phone_number}"
    document = user.dict()
    document.update({'_id': doc_id})
    db_instance: Database = get_bucket()
    _tuple_object = db_instance.save(document)
    return True


async def put_driver_ride_details(ride_object: DriverLogsRequest):
    doc_id = f"{RIDE_DOC_TYPE}::{ride_object.phone_number}"

    driver_data: Document = await get_driver_ride_details(ride_object.phone_number)
    new_ride_details = {
        "end_time": ride_object.end_time.isoformat(),
        "start_time": ride_object.start_time.isoformat(),
        "distance": ride_object.distance_travelled
    }
    db_instance: Database = get_bucket()
    if driver_data:
        if driver_data.get(ride_object.end_time.isoformat()):
            raise HTTPException(detail="Ride exists already", status_code=400)
        driver_data.update({ride_object.end_time.isoformat(): new_ride_details})
        _tuple_object = db_instance.save(driver_data)
    else:
        new_doc = {
            ride_object.end_time.isoformat(): new_ride_details
        }
        new_doc.update({'_id': doc_id})
        print(new_doc)
        _tuple_object = db_instance.save(new_doc)

    return True


async def get_driver_ride_details(phone_number: str):
    doc_id = f"{RIDE_DOC_TYPE}::{phone_number}"
    db_instance: Database = get_bucket()
    result: Document = db_instance.get(doc_id)
    if not result:
        return None
    return result


async def get_ride_details(phone_number: str, end_time: str):
    doc_id = f"{RIDE_DOC_TYPE}::{phone_number}"
    db_instance: Database = get_bucket()
    result: Document = db_instance.get(doc_id)
    ride_details: dict = result.get(end_time, None)
    if not ride_details:
        return None
    return ride_details
