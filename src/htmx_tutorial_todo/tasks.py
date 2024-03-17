from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass
class Task:
    title: str
    done: bool
    id: Optional[int] = None


class Storage(Protocol):
    def get(self, id_: int) -> Optional[Task]:
        """Return the item with the given id. If the item does not exist, return *None*"""
        ...

    def list(self) -> list[Task]:
        """Return a list of items that match the given filters. If no filters are given, return all items."""
        ...

    def set(self, task: Task) -> int:
        """Return the id of the created or updated item."""
        ...

    def update(self, id_: int, updates: dict) -> None:
        """Update the item with the given id. If the item does not exist, raise a ValueError."""
        ...

    def delete(self, key: int) -> Task:
        """Return the deleted item."""
        ...

    def counts(self) -> tuple[int, int]:
        """Return the tuple with (completed, total) tasks."""
        ...

    def shutdown(self) -> None:
        """Do the cleanup before closing the storage."""
        ...


def list_tasks(storage: Storage) -> list[Task]:
    return storage.list()


def get_task(storage: Storage, id_: int) -> Optional[Task]:
    return storage.get(id_)


def set_task(storage: Storage, task: Task) -> Task:
    id_ = storage.set(task)
    return Task(id=id_, title=task.title, done=task.done)


def update_task(storage: Storage, id_: int, updates: dict) -> None:
    return storage.update(id_, updates)


def delete_task(storage: Storage, id_: int) -> Task:
    return storage.delete(id_)


def count_tasks(storage: Storage) -> tuple[int, int]:
    return storage.counts()
