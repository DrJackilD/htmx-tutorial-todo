from typing import Optional

import tinydb

from .tasks import Task


class DatabaseTaskStorage:
    def __init__(self, db_name: str = "db.json"):
        self.db = tinydb.TinyDB(db_name)

    def get(self, id_: int) -> Optional[Task]:
        """Return the item with the given id. If the item does not exist, return *None*"""
        if doc := self.db.get(doc_id=id_):
            return Task(id=doc.doc_id, **doc)
        return None

    def list(self) -> list[Task]:
        """Return a list of items that match the given filters. If no filters are given, return all items."""
        return [Task(id=doc.doc_id, **doc) for doc in self.db.all()]

    def set(self, task: Task) -> int:
        """Return the id of the created or updated item."""
        return self.db.insert({"title": task.title, "done": task.done})

    def update(self, id_: int, updates: dict) -> None:
        """Update the item with the given id. If the item does not exist, raise a ValueError."""
        self.db.update(updates, doc_ids=[id_])

    def delete(self, id_: int) -> Task:
        """Return the deleted item."""
        task = self.db.get(doc_id=id_)
        self.db.remove(doc_ids=[id_])
        return Task(id=task.doc_id, **task)

    def counts(self) -> tuple[int, int]:
        """Return the tuple with (completed, total) tasks."""
        return self.db.count(tinydb.Query().done == True), len(self.db.all())  # noqa: E712

    def shutdown(self) -> None:
        """Do the cleanup before closing the storage."""
        self.db.close()
