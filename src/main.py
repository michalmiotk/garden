import threading
import json
import queue
import time
from collections import deque

from fastapi import FastAPI, Request, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import serial


from logs import log
from recv_item import RecvItem

baudrate = 115200
send_queue = queue.Queue()
recv_deque = deque(maxlen=10)

class SerialMock():
    def write(self, raw_data):
        log.info("I send"+str(raw_data))

serial_obj = serial.Serial('/dev/ttyACM0', baudrate)

def send_thread(serial_obj, send_queue):
    while True:
        if not send_queue.empty():
            raw_data = send_queue.get()
            serial_obj.write(raw_data + b'\n\r')


send_thread = threading.Thread(target=send_thread, args=(serial_obj, send_queue))
send_thread.daemon = True
send_thread.start()

def recv_thread(serial_obj, recv_deque):
    while serial_obj.isOpen():
        log.debug("begin of reading from serial")
        if serial_obj.inWaiting() > 0:
            try:
                raw_data = serial_obj.readline()
                log.info("received serial data" + str(raw_data))
                raw_data_without_trailer = raw_data.rstrip()
                log.info("I will put in recv deque" + str(raw_data_without_trailer))
                recv_item = RecvItem(raw_data_without_trailer)
                recv_deque.appendleft(recv_item)
            except TypeError as e:
                log.error(e)
            except json.decoder.JSONDecodeError as e:
                log.error(e)

recv_thread = threading.Thread(target=recv_thread, args=(serial_obj, recv_deque))
recv_thread.daemon = True
recv_thread.start()

def send(raw_data):
    send_queue.put(raw_data)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory="templates")

def serialize(dict_to_send: dict()) -> bytes:
    json_to_send = json.dumps(dict_to_send)
    return json_to_send.encode('utf-8')

@app.post("/set_temp/{temp}")
async def set_temp(temp: int = Path(title="temp which I will try to set in Celsius Degree", ge=-273, le=3000)):
    dict_to_send = {'temp': temp}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    return dict_to_send

@app.post('/set_air_humidity/{humidity_percent}')
async def set_air_humidity(humidity_percent: int=Path(ge=0, le=100)):
    dict_to_send = {'air_humidity': humidity_percent}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    return dict_to_send

@app.post('/set_soil_humidity/{humidity_percent}')
async def set_soil_humidity(humidity_percent: int=Path(ge=0, le=100)):
    dict_to_send = {'soil_humidity': humidity_percent}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    return dict_to_send

@app.post('/set_lightning/{lightning_percent_power}')
async def set_lightning(lightning_percent_power: int=Path(ge=0, le=100)):
    dict_to_send = {'lightning_percent_power': lightning_percent_power}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    return dict_to_send

@app.post("/set_fan_speed/{fan_speed}")
async def natural_lightning(fan_speed: int=Path(ge=0, le=100)):
    dict_to_send = {'fan_speed': fan_speed}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    return dict_to_send

@app.post("/air_out")
async def air_out():
    dict_to_send = {'cmd': 'air_out'}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    return dict_to_send

@app.post("/water")
async def water():
    dict_to_send = {'cmd': 'water'}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    return dict_to_send

@app.post("/natural_lightning")
async def natural_lightning():
    dict_to_send = {'cmd': 'natural_lightning'}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    return dict_to_send


def filter_deque(in_deque: deque, desired_key: str) -> "RecvItem or str":
    for item in in_deque:
        if item.is_actual():
            for key in item.recv_dict.keys():
                if key == desired_key:
                    return item
    return "not found response from arduino in deque" + str(in_deque)

##### GETTERS #####

@app.get("/temp_inside")
async def temp_inside():
    dict_to_send = {'get': 'temp_inside'}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    time.sleep(1)

    return filter_deque(recv_deque, "temp_inside")

@app.get("/temp_outside")
async def temp_outside():
    dict_to_send = {'get': 'temp_outside'}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    time.sleep(1)

    return filter_deque(recv_deque, "temp_outside")

@app.get("/air_humidity")
async def air_humidity():
    dict_to_send = {'get': 'air_humidity'}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    time.sleep(1)

    return filter_deque(recv_deque, "air_humidity")

@app.get("/soil_humidity")
async def soil_humidity():
    dict_to_send = {'get': 'soil_humidity'}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    time.sleep(1)

    return filter_deque(recv_deque, "soil_humidity")

@app.get("/lightning")
async def lightning():
    """
    returns lightning PWM ??
    """
    dict_to_send = {'get': 'lightning'}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    time.sleep(1)

    return filter_deque(recv_deque, "lightning")

@app.get("/water_tank_state")
async def water_tank_state():
    """
    returns water_tank_state in some units ????
    """
    dict_to_send = {'get': 'water_tank_state'}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    time.sleep(1)

    return filter_deque(recv_deque, "water_tank_state")

@app.get("/battery")
async def battery():
    """
    returns batery_percent - integer
    """
    dict_to_send = {'get': 'battery'}
    bytes_to_send = serialize(dict_to_send)
    send(bytes_to_send)
    time.sleep(1)

    return filter_deque(recv_deque, "battery")

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
