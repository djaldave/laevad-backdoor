#!/usr/bin/python
import socket


# create simple connection
# ipv4 run over tcp
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1",54321))
s.listen(5) # connection
print("listening for incoming connection")
target , ip = s.accept() # accept the connection
print("connected")
s.close()
