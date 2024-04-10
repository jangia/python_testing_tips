import sqlite3

import pytest

from models import Task, TaskStatus
from store import TaskStoreSQLite, TaskStore, TaskStoreInMemory


class TaskStoreContract:
    @pytest.fixture
    def store(self) -> TaskStore:
        raise NotImplementedError

    def test_added_task_listed(self, store: TaskStore):
        task = Task(title="Do the dishes", status=TaskStatus.OPEN, owner="johndoe")

        store.add_task(task)

        assert store.list_open(owner=task.owner) == [task]

    def test_closed_task_not_listed_in_open_tasks(self, store: TaskStore):
        task = Task(title="Do the dishes", status=TaskStatus.CLOSED, owner="johndoe")

        store.add_task(task)

        assert store.list_open(owner=task.owner) == []

    def test_task_from_other_owner_not_listed_in_open_tasks(self, store: TaskStore):
        task = Task(title="Do the dishes", status=TaskStatus.OPEN, owner="johndoe")

        store.add_task(task)

        assert store.list_open(owner="anotherowner") == []


class TestTaskStoreSQLite(TaskStoreContract):
    @pytest.fixture
    def connection(self, tmp_path) -> sqlite3.Connection:
        connection = sqlite3.connect(tmp_path / "test.db")
        connection.execute("CREATE TABLE tasks (title TEXT, status TEXT, owner TEXT)")
        return connection

    @pytest.fixture
    def store(self, connection) -> TaskStore:
        return TaskStoreSQLite(connection)


class TestTaskStoreInMemory(TaskStoreContract):
    @pytest.fixture
    def store(self) -> TaskStore:
        return TaskStoreInMemory()
