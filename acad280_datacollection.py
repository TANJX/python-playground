from ctypes import windll, Structure, c_long, byref
import time
import win32process, win32gui
import wmi


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return {"x": pt.x, "y": pt.y}


c = wmi.WMI()


def get_app_name(hwnd):
    """Get applicatin filename given hwnd."""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = p.Name
            return exe
    except:
        return None


while True:
    pos = queryMousePosition()
    print(','.join([str(time.time()),
                    str(pos['x']), str(pos['y']),
                    get_app_name(win32gui.GetForegroundWindow()),
                    win32gui.GetWindowText(win32gui.GetForegroundWindow())
                    ]))
    time.sleep(1)
