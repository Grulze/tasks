from pydantic import BaseModel, field_validator
from datetime import datetime


class AddTask(BaseModel):
    customer: str
    executor: str | None = 'Global'
    description: str
    time_limit: int | None = 24

    @field_validator('time_limit', mode='before')
    def time_limit_must_be_difit(cls, v):
        if not v.isdigit():
            return None
        return v

    @field_validator('executor')
    def name_must_contain_space(cls, v):
        print(v)
        if v == '':
            return None
        return v


class GetTask(AddTask):
    id: int
    completed: bool
    time_create: datetime
