import pytest
import baby_tracker.sleep.endpoints as endpoints
import baby_tracker.db as db
from datetime import datetime, timedelta


@pytest.fixture
def db_conn():
    _db_conn = db.init_db(db_file=":memory:")
    yield _db_conn
    _db_conn.close()


def test_handle_start_sleep_produce_valid_response(db_conn):
    args = ["start"]
    resp = endpoints.handle_sleep_request(args, db_conn)
    assert "error" not in resp["text"]


def test_handle_start_sleep_creates_an_incomplete_sleep_record(db_conn):
    args = ["start"]
    endpoints.handle_sleep_request(args, db_conn)

    id, from_time, to_time, duration, created_at, updated_at = \
        db.get_latest_sleep_records(db_conn, n=1)[0]
    now = datetime.now()
    one_second = timedelta(seconds=1)
    one_second_ago = now - one_second
    assert one_second_ago < from_time < now
    assert to_time is None
    assert duration is None
    assert from_time  < created_at < from_time + one_second
    assert updated_at is None

def test_handle_end_sleep_produce_error_with_no_active_sleep_stretch(db_conn):
    args = ["end"]
    with pytest.raises(endpoints.NoActiveSleepRecordError):
        endpoints.handle_sleep_request(args, db_conn)


def test_handle_end_sleep_produces_valid_response_with_active_sleep_stretch(db_conn):
    from_time = db.to_iso(datetime.now()) 
    endpoints.create_sleep_record([from_time], db_conn)
    resp = endpoints.handle_sleep_request(["end"], db_conn)
    assert "error" not in resp["text"]
