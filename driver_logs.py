import os

from fastapi import APIRouter, HTTPException

import memory_client
from couchDB_client import is_user_present, put_driver_ride_details, get_driver_ride_details
from models import DriverLogsRequest

DB_TYPE = os.environ.get("DB_TYPE", "in-memory")
driver_logs_router = APIRouter()


@driver_logs_router.post("/driver/logs/")
async def driver_logs(req: DriverLogsRequest):
    if DB_TYPE == "in-memory":
        result = await memory_client.is_user_present(req.phone_number)
    else:
        result = await is_user_present(req.phone_number)
    if result:
        result.update({"message": "user has found"})
    else:
        return {"message": "user has not found"}

    if DB_TYPE == "in-memory":
        result = await memory_client.put_driver_data(dlr=req)
        if result:
            return {"message": "driver data has been added"}
    else:
        flag = await put_driver_ride_details(ride_object=req)
        if flag:
            return {"message": "ride details added"}
    raise HTTPException(detail="something went wrong", status_code=400)


@driver_logs_router.get("/driver/logs/{phone_number}")
async def driver_logs_data(phone_number: str):
    if DB_TYPE == "in-memory":
        result = await memory_client.is_user_present(phone_number)
    else:
        result = await is_user_present(phone_number)
    if result:
        result.update({"message": "user has found"})
    else:
        raise HTTPException(detail=f"No user is present with {phone_number}", status_code=400)

    if DB_TYPE == "in-memory":
        ride_details = await memory_client.get_driver_data(phone_number)
    else:
        ride_details = await get_driver_ride_details(phone_number)
    if ride_details:
        return ride_details
    else:
        raise HTTPException(detail=f"No Ride details is present with {phone_number}", status_code=400)
