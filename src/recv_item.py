import json
from datetime import datetime, timedelta

class RecvItem():
    def __init__(self, recv_bytes):
        self.recv_dict = self.bytes_to_dict(recv_bytes)
        self.recv_time = datetime.now()

    def bytes_to_dict(self, in_bytes: bytes) -> dict:
        in_str = in_bytes.decode('utf-8')
        in_json = json.loads(in_str)
        return in_json

    def is_actual(self):
        outdate_val = 10
        time_difference = datetime.now() - self.recv_time
        return time_difference < timedelta(seconds=outdate_val)

    def __gt__(self, other_recv_item: "RecvItem"):
        return other_recv_item.recv_time > self.recv_time

    def __str__(self):
        return str(self.recv_dict) + " recv on " + str(self.recv_time)