from collections import defaultdict
from typing import Optional
from unittest.mock import call

import pytest
from bottle import Bottle, template
from webtest import TestApp

from htmx_tutorial_todo.api import Api
from htmx_tutorial_todo.db import DatabaseTaskStorage
from htmx_tutorial_todo.tasks import Storage, Task


class RecordingDbStorage(DatabaseTaskStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calls: dict[str, list[call]] = defaultdict(list)

    def set(self, task: Task) -> int:
        self.calls["set"].append(call(task))
        return super().set(task)

    def get(self, task_id: int) -> Optional[Task]:
        self.calls["get"].append(call(task_id))
        return super().get(task_id)

    def list(self) -> list[Task]:
        self.calls["list"].append(call())
        return super().list()

    def update(self, task_id: int, data: dict):
        self.calls["update"].append(call(task_id, data))
        return super().update(task_id, data)

    def delete(self, task_id: int):
        self.calls["delete"].append(call(task_id))
        return super().delete(task_id)

    def counts(self) -> tuple[int, int]:
        self.calls["counts"].append(call())
        return super().counts()


@pytest.fixture
def recording_storage() -> RecordingDbStorage:
    db = RecordingDbStorage("test_db.json")
    yield db
    db.db.truncate()


@pytest.fixture
def api(recording_storage: Storage) -> Api:
    return Api(Bottle(), recording_storage)


def test_index(api: Api, recording_storage: RecordingDbStorage):
    test_app = TestApp(api.app)
    response = test_app.get("/")
    assert recording_storage.calls["list"] == [call()]
    assert recording_storage.calls["counts"] == [call()]
    assert response.status_code == 200
    assert "Todo" in response.html.find("h1").text
    assert "(0/0)" in response.html.find("h1").find("span").text


def test_add(api: Api, recording_storage: RecordingDbStorage):
    test_app = TestApp(api.app)
    response = test_app.post("/tasks", {"title": "test"})
    assert recording_storage.calls["set"] == [call(Task(title="test", done=False))]
    assert response.status_code == 200
    assert response.text == template("_task", task=Task(title="test", done=False, id=1))


def test_set_task_status(api: Api, recording_storage: RecordingDbStorage):
    recording_storage.set(Task(title="test", done=False))
    recording_storage.set(Task(title="test2", done=False))
    test_app = TestApp(api.app)
    response = test_app.put("/tasks/1", {"task": ["1"]})
    assert recording_storage.calls["update"] == [
        call(1, {"done": True}),
    ]
    assert response.status_code == 200
    assert response.text == template("_task", task=Task(title="test", done=True, id=1))


def test_delete_task(api: Api, recording_storage: RecordingDbStorage):
    recording_storage.set(Task(title="test", done=False))
    test_app = TestApp(api.app)
    response = test_app.delete("/tasks/1")
    assert recording_storage.calls["delete"] == [call(1)]
    assert response.status_code == 200
