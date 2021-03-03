import time

from fastapi import APIRouter
from fastapi import BackgroundTasks

back_ground_task_router = APIRouter()


def do_background_task_processing(count: int):
    for _ in range(0, count):
        time.sleep(1)
        print("hello from back-ground-tasks", time.time())


@back_ground_task_router.get("/background-task")
def do_background_processing(count: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(do_background_task_processing, count)
    return {"message": "background-task called"}
