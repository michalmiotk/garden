from recv_item import RecvItem
import json
from datetime import datetime, timedelta

import pytest

@pytest.fixture
def json_bytes():
    desired_dict = {'cmd': 'pour'}
    some_json = json.dumps(desired_dict)
    json_bytes = some_json.encode('utf-8')
    return json_bytes

@pytest.fixture
def desired_dict():
    return {'cmd': 'pour'}

def test_serialize(json_bytes, desired_dict):
    recv_item = RecvItem(json_bytes)
    assert(recv_item.recv_dict == desired_dict)

def test_time_when_time_is_actual(json_bytes):
    recv_item = RecvItem(json_bytes)
    recv_item.recv_time = datetime.now() - timedelta(seconds=3)
    assert recv_item.is_actual() == True

def test_time_when_time_is_not_actual(json_bytes):
    recv_item = RecvItem(json_bytes)
    recv_item.recv_time = datetime.now() - timedelta(seconds=15)
    assert recv_item.is_actual() == False

def test_gt_operator(json_bytes):
    new_recv_item = RecvItem(json_bytes)
    old_recv_item = recv_item = RecvItem(json_bytes)
    old_recv_item.recv_time - timedelta(seconds=5)
    assert new_recv_item > old_recv_item 
