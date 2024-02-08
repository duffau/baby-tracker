from baby_tracker.db import _create_duration_record
from baby_tracker.router._duration import create_duration_record


def create_feed(conn, feed):
    return _create_duration_record(conn, feed, "feed")


def create_feed_record(args, db_conn):
    return create_duration_record(args, create_feed, db_conn)