import sqlite3
from abc import ABC

from models import Task, TaskStatus


class TaskStore(ABC):
    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def list_open(self, owner: str) -> list[Task]:
        raise NotImplementedError


class TaskStoreSQLite(TaskStore):
    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection

    def add_task(self, task: Task) -> None:
        self._connection.execute(
            "INSERT INTO tasks (title, status, owner) VALUES (?, ?, ?)",
            (task.title, task.status.name, task.owner),
        )

    def list_open(self, owner: str) -> list[Task]:
        cursor = self._connection.execute(
            "SELECT title, status, owner FROM tasks WHERE status = 'OPEN' AND owner = ?",
            (owner,),
        )
        return [
            Task(title, TaskStatus(status), owner)
            for title, status, owner in cursor.fetchall()
        ]
