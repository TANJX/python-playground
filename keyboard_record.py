import keyboard

keys = '`123456qwertasdfgzxcvnmp[]l'

def on_key():
    print(' was pressed')


keyboard.add_hotkey(' ', on_key)
keyboard.add_hotkey('z', on_key)
keyboard.wait()
