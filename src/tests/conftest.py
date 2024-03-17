import pytest

from htmx_tutorial_todo.db import DatabaseTaskStorage


@pytest.fixture
def db():
    yield DatabaseTaskStorage("test_db.json")
    DatabaseTaskStorage("test_db.json").db.truncate()
