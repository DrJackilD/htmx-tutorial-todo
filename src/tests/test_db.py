from htmx_tutorial_todo.tasks import Task


def test_set(db):
    assert db.set(Task(title="test", done=False)) == 1
    assert db.set(Task(title="test", done=False)) == 2


def test_get(db):
    db.set(Task(title="test", done=False))
    assert db.get(1) == Task(title="test", done=False, id=1)


def test_list(db):
    assert db.list() == []
    db.set(Task(title="test", done=False))
    assert db.list() == [Task(title="test", done=False, id=1)]


def test_update(db):
    db.set(Task(title="test", done=False))
    db.update(1, {"title": "test", "done": True})
    assert db.list() == [Task(title="test", done=True, id=1)]


def test_delete(db):
    db.set(Task(title="test", done=False))
    assert db.delete(1) == Task(title="test", done=False, id=1)
    assert db.list() == []


def test_counts(db):
    db.set(Task(title="test", done=False))
    assert db.counts() == (0, 1)
    db.update(1, {"title": "test", "done": True})
    assert db.counts() == (1, 1)
