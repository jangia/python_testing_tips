import sqlite3
from abc import ABC

from behavior.models import Task, TaskStatus


class TaskStore(ABC):
    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def list_tasks(self) -> list[Task]:
        raise NotImplementedError


class TaskStoreSQLite(TaskStore):
    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection

    def add_task(self, task: Task) -> None:
        self._connection.execute(
            "INSERT INTO tasks (title, status) VALUES (?, ?)",
            (task.title, task.status.name),
        )

    def list_tasks(self) -> list[Task]:
        cursor = self._connection.execute("SELECT title, status FROM tasks")
        return [Task(title, TaskStatus(status)) for title, status in cursor.fetchall()]


class TaskStoreInMemory(TaskStore):
    def __init__(self):
        self._tasks = []

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def list_tasks(self) -> list[Task]:
        return self._tasks
