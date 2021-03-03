import couchdb
from couchdb import Database, Document
from fastapi import APIRouter

from models import RegisterUserRequest as User

database_router = APIRouter()

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
    doc_id = f"userprofile::{user.phone_number}"
    document = user.dict()
    document.update({'_id': doc_id})
    db_instance: Database = get_bucket()
    _tuple_object = db_instance.save(document)
    return True
