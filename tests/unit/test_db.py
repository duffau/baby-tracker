import pytest
from datetime import datetime, timedelta

from baby_tracker import db


TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

@pytest.fixture
def db_conn():
    _db_conn = db.init_db(db_file=":memory:")
    yield _db_conn
    _db_conn.close()


def make_feed_record(
    from_time = datetime(2021, 5, 18, 6, 38, 30),
    to_time = datetime(2021, 5, 18, 6, 50, 20)
):
    duration = to_time - from_time
    return (from_time, to_time, duration)


def list_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return [table_row[0] for table_row in tables]


def test_create_connection():
    conn = db.create_connection(db_file=":memory:")
    tables = list_tables(conn)
    assert tables == []
    conn.close()


def test_create_table():
    conn = db.create_connection(db_file=":memory:")
    db.create_table(conn, "CREATE TABLE mytable ( mycol );")
    db.create_table(conn, "CREATE TABLE myothertable ( mycol );")
    tables = list_tables(conn)
    assert tables == ["mytable", "myothertable"]


def test_init_db(db_conn):
    tables = list_tables(db_conn)
    assert tables == ["feed", "sleep", "weight", "poop"]
    db_conn.close()


def test_create_feed(db_conn):
    feed_record = make_feed_record()
    feed_id = db.create_feed(db_conn, feed_record)
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM feed where id = ?;", (feed_id,))
    rows = cursor.fetchall()
    assert len(rows) == 1


def test_get_feed_record(db_conn):
    from_time, to_time, duration = make_feed_record()
    feed_id = db.create_feed(db_conn, (from_time, to_time, duration))
    feed_record = db.get_feed_record_by_id(db_conn, feed_id)
    _id, _from_time, _to_time, _duration, _created_at, _updated_at = feed_record
    assert _id == feed_id
    assert _from_time == from_time
    assert _to_time == to_time
    assert _duration == duration
    assert _created_at < datetime.now()
    assert _created_at > datetime.now()-timedelta(seconds=1 )
    assert _updated_at is None
