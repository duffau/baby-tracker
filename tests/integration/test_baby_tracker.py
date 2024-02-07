import os
import requests
import re
import pytest

SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = os.getenv("SERVER_PORT")
BASE_URL = f"http://{SERVER_IP}:{SERVER_PORT}/babytracker"

@pytest.fixture
def create_feed_record():
    resp = requests.post(BASE_URL + "/feed", data={"text": "12:30 12:35"})
    resp.raise_for_status()
    assert "error" not in resp.json()["text"]
    yield
    resp = requests.post(BASE_URL + "/feed", data={"text": "d 1"})
    resp.raise_for_status()
    assert "error" not in resp.json()["text"]

@pytest.fixture
def create_sleep_record():
    resp = requests.post(BASE_URL + "/sleep", data={"text": "12:30 12:35"})
    resp.raise_for_status()
    assert "error" not in resp.json()["text"]
    yield
    resp = requests.post(BASE_URL + "/sleep", data={"text": "d 1"})
    resp.raise_for_status()
    assert "error" not in resp.json()["text"]


def test_is_up():
    resp = requests.post(BASE_URL)
    assert resp.status_code == 200
    print(resp.text)

class TestFeedEndpoints:
    def test_create_feed_record(self):
        params = {"text": "12:30 12:35"}
        resp = requests.post(BASE_URL + "/feed", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

        params = {"text": "list"}
        resp = requests.post(BASE_URL + "/feed", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]
        assert "12:30" in resp.json()["text"]
        assert "00:05" in resp.json()["text"]

        params = {"text": "d 1"}
        resp = requests.post(BASE_URL + "/feed", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

    def test_start_end_feed(self):
        params = {"text": "s 12:30"}
        resp = requests.post(BASE_URL + "/feed", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

        params = {"text": "e 12:35"}
        resp = requests.post(BASE_URL + "/feed", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]
        assert "00:05" in resp.json()["text"]


class TestAnalyzeFeedEndpoints:
    def test_analyze_total(self, create_feed_record):
        params = {"text": "analyze total"}
        resp = requests.post(BASE_URL + "/feed", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

    def test_analyze_avg(self, create_feed_record):
        params = {"text": "analyze avg"}
        resp = requests.post(BASE_URL + "/feed", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

    def test_analyze_timeline(self, create_feed_record):
        params = {"text": "analyze timeline"}
        resp = requests.post(BASE_URL + "/feed", data=params)
        assert resp.status_code == 200
        print(resp.json())


class TestSleepEndpoints:
    def test_create_list_delete_sleep_record(self):
        params = {"text": "12:30 12:35"}
        resp = requests.post(BASE_URL + "/sleep", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

        params = {"text": "list"}
        resp = requests.post(BASE_URL + "/sleep", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]
        assert "12:30" in resp.json()["text"]
        assert "00:05" in resp.json()["text"]

        params = {"text": "d 1"}
        resp = requests.post(BASE_URL + "/sleep", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

    def test_start_end_sleep(self):
        params = {"text": "s 12:30"}
        resp = requests.post(BASE_URL + "/sleep", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

        params = {"text": "e 12:35"}
        resp = requests.post(BASE_URL + "/sleep", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]
        assert "00:05" in resp.json()["text"]

class TestAnalyzeSleepEndpoints:
    def test_analyze_total(self, create_sleep_record):
        params = {"text": "analyze total"}
        resp = requests.post(BASE_URL + "/sleep", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

    def test_analyze_avg(create_sleep_record):
        params = {"text": "analyze avg"}
        resp = requests.post(BASE_URL + "/sleep", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

    def test_analyze_timeline(create_sleep_record):
        params = {"text": "analyze timeline"}
        resp = requests.post(BASE_URL + "/sleep", data=params)
        assert resp.status_code == 200
        print(resp.json())



class TestWeightEndpoints:

    def test_create_list_delete_weight_record(self):
        params = {"text": "2021-05-18 3254"}
        resp = requests.post(BASE_URL + "/weight", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

        params = {"text": "2021-05-22 3300"}
        resp = requests.post(BASE_URL + "/weight", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

        params = {"text": "2021-05-25 3400"}
        resp = requests.post(BASE_URL + "/weight", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

        params = {"text": "ls"}
        resp = requests.post(BASE_URL + "/weight", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

        params = {"text": "d 1"}
        resp = requests.post(BASE_URL + "/weight", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

    def test_analyze_weight(self):
        params = {"text": "analyze"}
        resp = requests.post(BASE_URL + "/weight", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

class TestPoopEndpoints:


    def test_create_list_delete_analyze_poop_record(self):
        params = {"text": "2021-05-18"}
        resp = requests.post(BASE_URL + "/poop", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

        params = {"text": "ls"}
        resp = requests.post(BASE_URL + "/poop", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]

        params = {"text": "d 1"}
        resp = requests.post(BASE_URL + "/poop", data=params)
        assert resp.status_code == 200
        print(resp.json())
        assert "error" not in resp.json()["text"]
