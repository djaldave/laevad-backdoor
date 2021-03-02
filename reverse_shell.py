#!/usr/bin/python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 and TCP
sock.connect(("127.0.0.1", 54321))
print("connection establish to server")

while True:
	command = sock.recv(1024) # receive bytes
	print(command)
	if command  == "q":
		break
	else:
		command_back = raw_input("input command: ")
		sock.send(command_back)
sock.close()
