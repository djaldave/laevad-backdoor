#!/usr/bin/python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 and TCP
sock.connect(("127.0.0.1", 54321))
print("connection establish to server")
sock.close()
