# Tasks
This app is like a big notepad with tasks. 
There you can create, execute, delete and search for tasks that you need.

## 1 - Installing dependencies.

```sh
pip install -r requirements.txt
```

## 2 - Setup database.

You need to install Postgresql with the
user "postgres" and the password "postgres" 
(or change the async_eng settings in the file
database.py ), and create a database named 
"taskdb" (or you can also change it in 
database.py).

```sh
CREATE DATABASE taskdb;
```

Then you need to run the python function
to create a table.

```sh
python -c 'import database; database.create_table()'
```

## 3 - Start server.

To start the server, run the command:

```sh
uvicorn main:my_app
```

Now the server is running and is located at the link http://127.0.0.1:8000