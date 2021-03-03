import asyncio

from fastapi import APIRouter

async_router = APIRouter()


async def wait_for_a_sec():
    await asyncio.sleep(1)


async def print_statement():
    print("first comment")
    await wait_for_a_sec()
    print("second comment")


@async_router.get("/async-call")
async def async_call():
    await asyncio.gather(print_statement(), print_statement(), print_statement())
    return {"message": "all done"}
