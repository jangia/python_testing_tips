import sqlite3

import pytest

from behavior.models import Task, TaskStatus
from behavior.store import TaskStoreInMemory, TaskStoreSQLite


@pytest.fixture
def connection(tmp_path) -> sqlite3.Connection:
    connection = sqlite3.connect(tmp_path / "test.db")
    connection.execute("CREATE TABLE tasks (title TEXT, status TEXT)")
    return connection


@pytest.fixture
def store(connection) -> TaskStoreSQLite:
    return TaskStoreSQLite(connection)


def test_added_task_listed(store: TaskStoreSQLite):
    task = Task(title="Do the dishes", status=TaskStatus.OPEN)

    store.add_task(task)

    assert store.list_tasks() == [task]


@pytest.fixture
def store_() -> TaskStoreInMemory:
    return TaskStoreInMemory()


def test_added_task_listed_(store_: TaskStoreInMemory):
    task = Task(title="Do the dishes", status=TaskStatus.OPEN)

    store_.add_task(task)

    assert store_.list_tasks() == [task]
