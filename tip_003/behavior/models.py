from dataclasses import dataclass
from enum import Enum


class TaskStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass
class Task:
    title: str
    status: TaskStatus
