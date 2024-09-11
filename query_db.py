from typing import List
from sqlalchemy import select, update, delete
from database import TaskDB, session
from schema import AddTask, GetTask


async def get_task_db(executor: str | None = None) -> List[GetTask]:
    async with session() as ses:
        if executor:
            query = select(TaskDB).where(TaskDB.executor == executor)
        else:
            query = select(TaskDB)
        response = await ses.execute(query)
        task_set = response.scalars().all()
        for task in task_set:
            task.time_create = task.time_create.replace(microsecond=0)
        return task_set


async def add_task_db(task: AddTask):
    async with session() as ses:
        task_data = task.model_dump()
        task_bd = TaskDB(**task_data)
        ses.add(task_bd)
        await ses.commit()


async def closing_task_db(task_id: int):
    async with session() as ses:
        await ses.execute(update(TaskDB).where(TaskDB.id == task_id).values(completed=True))
        await ses.commit()


async def delete_task_db(task_id: int):
    async with session() as ses:
        await ses.execute(delete(TaskDB).where(TaskDB.id == task_id))
        await ses.commit()
