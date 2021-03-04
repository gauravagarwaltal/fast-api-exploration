import os

from fastapi import APIRouter

import memory_client
from models import (
    DriverLogsRequest,
)

DB_TYPE = os.environ.get("DB_TYPE", "in-memory")
driver_logs_router = APIRouter()


@driver_logs_router.post("/driver/logs/")
async def driver_logs(req: DriverLogsRequest):
    if DB_TYPE == "in-memory":
        result = await memory_client.is_user_present(req.phone_number)

    if result:
        result.update({"message": "user has found"})
    else:
        return {"message":"user has not found"}

    if DB_TYPE == "in-memory":
        result = await memory_client.put_driver_data(dlr=req)
        if result:
            return {"message":"driver data has been added"}
    return {"message":"something went wrong"}


@driver_logs_router.get("/driver/logs/{phone_number}")
async def driver_logs_data(phone_number: str):
    if DB_TYPE == "in-memory":
        result = await memory_client.is_user_present(phone_number)

    if result:
        result.update({"message": "user has found"})
    else:
        return {"message":"user has not found"}

    if DB_TYPE == "in-memory":
        result = await memory_client.get_driver_data(phone_number)
        if result:
            return result
        else:
            return {"message": "no data found"}

