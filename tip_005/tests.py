import sqlite3

import pytest

from models import Task, TaskStatus
from store import TaskStoreSQLite


@pytest.fixture
def connection(tmp_path) -> sqlite3.Connection:
    connection = sqlite3.connect(tmp_path / "test.db")
    connection.execute("CREATE TABLE tasks (title TEXT, status TEXT, owner TEXT)")
    return connection


@pytest.fixture
def store(connection) -> TaskStoreSQLite:
    return TaskStoreSQLite(connection)


def test_added_task_listed(store: TaskStoreSQLite):
    task = Task(title="Do the dishes", status=TaskStatus.OPEN, owner="johndoe")

    store.add_task(task)

    assert store.list_open(owner=task.owner) == [task]


def test_closed_task_not_listed_in_open_tasks(store: TaskStoreSQLite):
    task = Task(title="Do the dishes", status=TaskStatus.CLOSED, owner="johndoe")

    store.add_task(task)

    assert store.list_open(owner=task.owner) == []


def test_task_from_other_owner_not_listed_in_open_tasks(store: TaskStoreSQLite):
    task = Task(title="Do the dishes", status=TaskStatus.OPEN, owner="johndoe")

    store.add_task(task)

    assert store.list_open(owner="anotherowner") == []
