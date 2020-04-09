import json
import threading
import time
import copy
from ctypes import windll, Structure, c_long, byref

import requests
import win32gui
import win32process
import wmi

FREQUENCY = 20
MOVING_THRESHOLD = 7
BACKEND_DOMAIN = 'http://localhost'

blacklist = ['None']
location_data = []

# every minute save to cloud
count = 0
last_x = -1
last_y = -1

c = wmi.WMI()


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def query_mouse_position():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return {"x": pt.x, "y": pt.y}


pid_cache = {}


def get_app_name():
    """Get applicatin filename given hwnd."""
    try:
        _, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        if pid not in pid_cache:
            for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
                exe = p.Name
                pid_cache[pid] = exe
                return exe
        else:
            return pid_cache[pid]
    except:
        return ''


def get_app_text():
    """Get applicatin filename given hwnd."""
    try:
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except:
        return ''


def window_size(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))


def get_process_id(process_name):
    if process_name in process_name_map.keys():
        return process_name_map[process_name]
    elif process_name in local_process_name_map.keys():
        return local_process_name_map[process_name]
    else:
        _new_id = len(process_name_map) + len(local_process_name_map)
        local_process_name_map[process_name] = _new_id
        return _new_id


def save_local_process_map_to_cloud(_data):
    if len(_data) < 1:
        return
    _url = BACKEND_DOMAIN + "/acad280/processes"
    _payload = {'processes': _data}
    _response = requests.post(_url, json=_payload)
    # TODO post fail?
    _json = json.loads(_response.text)
    if 'count' not in _json.keys():
        print('error: save_local_process_map_from_cloud')
    elif _json['count'] != len(_data):
        print('error: save_local_process_map_from_cloud size different')
    for _name in _data.keys():
        process_name_map[_name] = _data[_name]
        del local_process_name_map[_name]
    print('processes saved ' + _response.text)


def get_process_map_from_cloud():
    _url = BACKEND_DOMAIN + "/acad280/processes"
    _response = requests.get(_url)
    return json.loads(_response.text)


def save_to_cloud(_data):
    if len(_data) < 1:
        return
    _url = BACKEND_DOMAIN + "/acad280/locations"
    _payload = {'locations': _data}
    _response = requests.post(_url, json=_payload)
    print('locations saved ' + _response.text)


if __name__ == "__main__":
    local_process_name_map = {}
    # fetch process name map
    process_name_map = get_process_map_from_cloud()

    time_count = []
    last_time = time.time()
    while True:
        try:
            # window_size(win32gui.GetForegroundWindow())
            pass
        except:
            continue
        pos = query_mouse_position()
        app_name = get_app_name()
        # app_text = get_app_text()
        processId = get_process_id(app_name)
        if app_name \
                and app_name not in blacklist \
                and abs(last_x - pos['x']) > MOVING_THRESHOLD \
                and abs(last_y - pos['y']) > MOVING_THRESHOLD:
            location_data.append({
                'time': time.time(),
                'positionX': pos['x'],
                'positionY': pos['y'],
                'processId': processId,
                'applicationName': 0,
            })
            last_x = pos['x']
            last_y = pos['y']
            print(str(pos['x']) + ', ' + str(pos['y']))
            time_count.append(time.time() - last_time)
            last_time = time.time()
        count += 1
        if count == 5 * FREQUENCY:
            print('saving...')
            print(sum(time_count) / len(time_count))
            threading.Thread(target=save_to_cloud, args=(copy.deepcopy(location_data),)).start()
            location_data.clear()
            threading.Thread(target=save_local_process_map_to_cloud,
                             args=(copy.deepcopy(local_process_name_map),)).start()
            count = 0
        time.sleep(1 / FREQUENCY)
