from typing import List
from fastapi import FastAPI, Depends, Request
from query_db import add_task_db, get_task_db, closing_task_db, delete_task_db
from schema import AddTask, GetTask
from fastapi.responses import RedirectResponse, HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from errors_response import from_and_description


my_app = FastAPI()
template = Jinja2Templates(directory='templates')


@my_app.get('/')
async def get_all_tasks(request: Request) -> HTMLResponse:
    """
    Returns html page with all tasks or those with the specified executor from database.
    :param request:
    :return: html page
    """
    executor = request.query_params.get('executor')
    tasks = await get_task_db(executor)
    return template.TemplateResponse('base.html', {'request': request, 'tasks': tasks})


@my_app.post('/')
async def new_task(request: Request) -> Response:
    """
    Adds a new task to the database.
    :param request:
    :return: html page
    """
    form = await request.form()
    if not form['time_limit'].isdigit():
        form._dict['time_limit'] = None
    if form['executor'] == '':
        form._dict['executor'] = None
    if form['customer'] == '' or form['description'] == '':
        return HTMLResponse(from_and_description, status_code=200)
    task = AddTask.model_validate(form)
    await add_task_db(task)
    return RedirectResponse('/', status_code=303)


@my_app.patch('/complete/{task_id}')
async def closing_task(task_id: int):
    """
    Sets task.completed with the passed task.id to the True state.
    :param task_id:
    """
    await closing_task_db(task_id)


@my_app.delete('/delete/{task_id}')
async def delete_task(task_id: int):
    """
    Deletes task with the passed task.id.
    :param task_id:
    """
    await delete_task_db(task_id)


@my_app.get('/nontemplate')
async def get_all_tasks_non(executor: str | None = None) -> List[GetTask]:
    """
    Returns all tasks or those with the specified executor from database.
    :param executor:
    :return: List[GetTask]
    """
    return await get_task_db(executor)


@my_app.post('/nontemplate')
async def new_task_non(task: AddTask = Depends()) -> str:
    """
    Adds a new task to the database.
    :param task:
    :return: List[AddTask]
    """
    await add_task_db(task)
    return "done"


@my_app.patch('/nontemplate')
async def closing_task_non(task_id: int) -> str:
    """
    Sets task.completed with the passed task.id to the True state.
    :param task_id:
    :return: List[GetTask]
    """
    await closing_task_db(task_id)
    return "done"


@my_app.delete('/nontemplate')
async def delete_task_non(task_id: int) -> str:
    """
    Deletes task with the passed task.id.
    :param task_id:
    """
    await delete_task_db(task_id)
    return "done"
