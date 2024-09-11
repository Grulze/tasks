from pydantic import BaseModel
from datetime import datetime


class AddTask(BaseModel):
    customer: str
    executor: str | None = 'Global'
    description: str
    time_limit: int | None = 24


class GetTask(AddTask):
    id: int
    completed: bool
    time_create: datetime
