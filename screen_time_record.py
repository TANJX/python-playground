import win32gui
import win32process
import wmi
from datetime import datetime
import time
from ctypes import windll, Structure, c_long, byref

DATA_FOLDER = "data/screen/"
BLACKLIST = ['', 'explorer', 'LockApp', 'ApplicationFrameHost',
             'Listary', 'Code', 'StartMenuExperienceHost', 'SearchApp', 'launcher', 'Taskmgr', 'IDMan', 'OneDrive']

c = wmi.WMI()


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def query_mouse_position():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return [pt.x, pt.y]


def get_app_name():
    """Get applicatin filename given hwnd."""
    try:
        _, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = p.Name
            return exe
    except:
        return ''


if __name__ == "__main__":
    last_mouse_location = [-1, -1]
    while True:
        try:
            mouse_location = query_mouse_position()
            moved = 1
            if mouse_location[0] == last_mouse_location[0] and mouse_location[1] == last_mouse_location[1]:
                moved = 0
            last_mouse_location = mouse_location
            now = datetime.fromtimestamp(time.time())
            app = get_app_name().replace('.exe', '')
            if app in BLACKLIST:
                continue
            line = '%d,%d,%s,%d\n' % (now.hour, now.minute, app, moved)
            f = open(DATA_FOLDER + str(now.date()) + '.txt', "a")
            f.write(line)
            f.close()
            print(line)
            time.sleep(60)
        except:
            continue
