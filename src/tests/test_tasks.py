from unittest import mock

import pytest

from htmx_tutorial_todo.tasks import (
    Task,
    count_tasks,
    delete_task,
    list_tasks,
    set_task,
    update_task,
)


@pytest.fixture
def storage():
    storage = mock.Mock()
    storage.list.return_value = []
    storage.set.return_value = 1
    storage.update.return_value = None
    storage.delete.return_value = {"title": "test", "done": False}
    return storage


def test_set(storage):
    assert set_task(storage, Task(title="test", done=False)) == Task(
        id=1, title="test", done=False
    )
    assert storage.set.call_args == mock.call(Task(title="test", done=False))


def test_list(storage):
    assert list_tasks(storage) == []
    assert storage.list.call_args == mock.call()


def test_update(storage):
    update_task(storage, 1, {"title": "test", "done": True})
    assert storage.update.call_args == mock.call(1, {"title": "test", "done": True})


def test_delete(storage):
    assert delete_task(storage, 1) == {"title": "test", "done": False}
    assert storage.delete.call_args == mock.call(1)


def test_counts(storage):
    storage.counts.return_value = (1, 0)
    assert count_tasks(storage) == (1, 0)
    assert storage.counts.call_args == mock.call()
    storage.counts.return_value = (1, 1)
    assert count_tasks(storage) == (1, 1)
    assert storage.counts.call_args == mock.call()
