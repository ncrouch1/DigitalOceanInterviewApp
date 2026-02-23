import uuid

import pytest

from db import DatabaseWrapper


def make_db():
    # Use a temporary file-based SQLite database so each connection
    # sees the same data (in-memory SQLite creates isolated DBs per connection).
    import tempfile

    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    return DatabaseWrapper(f"sqlite:///{tmp.name}")


def test_create_and_get_score():
    db = make_db()
    user_id = db.create_user("alice")
    assert isinstance(user_id, uuid.UUID)
    assert db.get_score(user_id) == 0


def test_update_score():
    db = make_db()
    user_id = db.create_user("bob")
    db.update_score(user_id, 42)
    assert db.get_score(user_id) == 42


def test_get_top_x_scores():
    db = make_db()
    u1 = db.create_user("u1")
    u2 = db.create_user("u2")
    u3 = db.create_user("u3")

    db.update_score(u1, 10)
    db.update_score(u2, 30)
    db.update_score(u3, 20)

    top2 = db.get_top_x_scores(2)
    assert len(top2) == 2
    assert top2[0]["username"] == "u2" and top2[0]["score"] == 30
    assert top2[1]["username"] == "u3" and top2[1]["score"] == 20


def test_get_user_with_neighbors():
    db = make_db()
    low = db.create_user("low")
    mid = db.create_user("mid")
    high = db.create_user("high")

    db.update_score(low, 10)
    db.update_score(mid, 20)
    db.update_score(high, 30)

    neighbors = db.get_user_with_neighbors(mid)
    assert neighbors["target"]["username"] == "mid"
    assert neighbors["target"]["score"] == 20
    assert neighbors["above"]["username"] == "high"
    assert neighbors["above"]["score"] == 30
    assert neighbors["below"]["username"] == "low"
    assert neighbors["below"]["score"] == 10


def test_get_user_with_neighbors_nonexistent():
    db = make_db()
    non = uuid.uuid4()
    neighbors = db.get_user_with_neighbors(non)
    assert neighbors == {"above": None, "target": None, "below": None}
import uuid

import pytest

from db import DatabaseWrapper


def make_db():
    return DatabaseWrapper("sqlite:///:memory:")


def test_create_and_get_score():
    db = make_db()
    user_id = db.create_user("alice")
    assert isinstance(user_id, uuid.UUID)
    assert db.get_score(user_id) == 0


def test_update_score():
    db = make_db()
    user_id = db.create_user("bob")
    db.update_score(user_id, 42)
    assert db.get_score(user_id) == 42


def test_get_top_x_scores():
    db = make_db()
    u1 = db.create_user("u1")
    u2 = db.create_user("u2")
    u3 = db.create_user("u3")

    db.update_score(u1, 10)
    db.update_score(u2, 30)
    db.update_score(u3, 20)

    top2 = db.get_top_x_scores(2)
    assert len(top2) == 2
    assert top2[0]["username"] == "u2" and top2[0]["score"] == 30
    assert top2[1]["username"] == "u3" and top2[1]["score"] == 20


def test_get_user_with_neighbors():
    db = make_db()
    low = db.create_user("low")
    mid = db.create_user("mid")
    high = db.create_user("high")

    db.update_score(low, 10)
    db.update_score(mid, 20)
    db.update_score(high, 30)

    neighbors = db.get_user_with_neighbors(mid)
    assert neighbors["target"]["username"] == "mid"
    assert neighbors["target"]["score"] == 20
    assert neighbors["above"]["username"] == "high"
    assert neighbors["above"]["score"] == 30
    assert neighbors["below"]["username"] == "low"
    assert neighbors["below"]["score"] == 10


def test_get_user_with_neighbors_nonexistent():
    db = make_db()
    non = uuid.uuid4()
    neighbors = db.get_user_with_neighbors(non)
    assert neighbors == {"above": None, "target": None, "below": None}
