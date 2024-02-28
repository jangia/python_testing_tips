import sqlite3

from implementation_details.models import Task, TaskStatus


class TaskStoreSQLite:
    def add_task(self, connection: sqlite3.Connection, task):
        connection.execute(
            "INSERT INTO tasks (title, status) VALUES (?, ?)",
            (task.title, task.status.name),
        )

    def list_tasks(
        self,
        connection: sqlite3.Connection,
    ):
        cursor = connection.execute("SELECT title, status FROM tasks")
        return [Task(title, TaskStatus(status)) for title, status in cursor.fetchall()]


class TaskStoreInMemory:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def list_tasks(self) -> list[Task]:
        return self.tasks
