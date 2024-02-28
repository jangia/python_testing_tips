import sqlite3

import pytest

from implementation_details.models import Task, TaskStatus
from implementation_details.store import TaskStoreSQLite, TaskStoreInMemory


@pytest.fixture
def connection(tmp_path) -> sqlite3.Connection:
    connection = sqlite3.connect(tmp_path / "test.db")
    connection.execute("CREATE TABLE tasks (title TEXT, status TEXT)")
    return connection


def test_add_task(connection: sqlite3.Connection):
    store = TaskStoreSQLite()
    task = Task(title="Do the dishes", status=TaskStatus.OPEN)

    store.add_task(connection, task)

    task_row = connection.execute("SELECT title, status FROM tasks").fetchone()
    assert task_row[0] == "Do the dishes"
    assert task_row[1] == "OPEN"


def test_list_tasks(connection: sqlite3.Connection):
    connection.execute(
        "INSERT INTO tasks (title, status) VALUES ('Do the dishes', 'OPEN')"
    )
    store = TaskStoreSQLite()

    assert store.list_tasks(connection) == [
        Task(title="Do the dishes", status=TaskStatus.OPEN)
    ]


def test_add_task_():
    store = TaskStoreInMemory()
    task = Task(title="Do the dishes", status=TaskStatus.OPEN)

    store.add_task(task)

    assert store.tasks[0].title == "Do the dishes"
    assert store.tasks[0].status == "OPEN"


def test_list_tasks_():
    store = TaskStoreInMemory()
    task = Task(title="Do the dishes", status=TaskStatus.OPEN)

    store.tasks.append(task)

    assert store.list_tasks() == [task]
