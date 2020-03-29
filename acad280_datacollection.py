from ctypes import windll, Structure, c_long, byref
import time
import win32process, win32gui
import wmi

FREQUENCY = 5
MOVING_THRESHOLD = 7

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


def get_app_name():
    """Get applicatin filename given hwnd."""
    try:
        _, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = p.Name
            return exe
    except:
        return ''


def get_app_text():
    """Get applicatin filename given hwnd."""
    try:
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except:
        return ''


def save_to_cloud():
    print(len(location_data))
    location_data.clear()
    pass


while True:
    pos = query_mouse_position()
    app_name = get_app_name()
    app_text = get_app_text()
    if app_name and abs(last_x - pos['x']) > MOVING_THRESHOLD and abs(last_y - pos['y']) > MOVING_THRESHOLD:
        location_data.append({
            'time': time.time(),
            'positionX': pos['x'],
            'positionY': pos['y'],
            'processId': str(time.time()),
            'applicationName': str(time.time()),
        })
        last_x = pos['x']
        last_y = pos['y']
        print(str(pos['x']) + ', ' + str(pos['y']))
    count += 1
    if count == 60 * FREQUENCY:
        save_to_cloud()
        count = 0
    time.sleep(1 / FREQUENCY)
