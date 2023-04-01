import requests
import json

"""
Here is the process:
1. You send your account ID and session ID to geoFS.
2. It sends you back myID.
3. You complete the handshake by sending it your account ID, Session ID, and ID.
4. Now you can use the API with the previous three tokens.

How to get your session ID.
1. Log into GEOFS on the account you want to use and join the game.
2. You can either use chrome dev tools to view past requests in order to get your session ID.
or you can manually get the value from your cookies.
The cookie name is 'PHPSESSID'
Look up a tutorial on how to view api requests on chrome, or use a tutorial on how to use your browsers cookies.
"""

def init_server_instance(geofs_session_id, returnMyId=False): # initializes connection and gains mandatory variables from server.
	# initializes server connection and gets details from server.
	body = {
		#You can basically just copy and paste this from an update request on the chrome dev tools network tab.
		"origin": "https://www.geo-fs.com",
		"acid":"707105", #replace this with your accounts session ID
		"sid":geofs_session_id, #GOOD GOD PLEASE PUT THIS IN A .env FILE. IF SOMEONE STEALS THIS THEY CAN TALK IN CHAT ON YOUR ACCOUNT.
		"id":"", #Your ID that GeoFS will give you. Leave it blank for now.
		"ac":"1",
		"co":[42.36021568682466,-70.98767598755524,4.589746820023676,-103.04273973572526,-15.919583740307557,-0.376840533503692],
		"ve":[2.7011560632672626e-10,7.436167948071671e-11,0.000004503549489433212,0,0,0],
		"st":{"gr":True,"as":0},
		"ti":1678751444055,
		"m":"", 
		"ci":0
	}
	try:
		#return the handshake
		response = requests.post(
			"https://mps.geo-fs.com/update",
			json = body,
			cookies = {"PHPSESSID": geofs_session_id}
		)
		print("Successfully connect to server.")
		response_body = json.loads(response.text)

		body2 = {
			"origin": "https://www.geo-fs.com",
			"acid":"701183",
			"sid":geofs_session_id,
			"id":response_body["myId"],
			"ac":"1",
			"co":[42.36021568682466,-70.98767598755524,4.589746820023676,-103.04273973572526,-15.919583740307557,-0.376840533503692],
			"ve":[2.7011560632672626e-10,7.436167948071671e-11,0.000004503549489433212,0,0,0],
			"st":{"gr":True,"as":0},
			"ti":1678751444055,
			"m":"", 
			"ci":response_body["lastMsgId"]
		}
		response = requests.post(
			"https://mps.geo-fs.com/update",
			json = body2,
			cookies = {"PHPSESSID": geofs_session_id}
		)
		response_body = json.loads(response.text)

		if returnMyId:
			return response_body["myId"], response_body["lastMsgId"]
		else:
			return response_body["myId"]
	except:
		print("Error code 1. Failed handshake.")

def sendMsg(myId, msg, geofs_session_id):
	body = {
		"origin": "https://www.geo-fs.com",
		"acid":"707105",
		"sid":geofs_session_id,
		"id":myId,
		"ac":"1",
		"co":[42.36021568682466,-70.98767598755524,4.589746820023676,-103.04273973572526,-15.919583740307557,-0.376840533503692],
		"ve":[2.7011560632672626e-10,7.436167948071671e-11,0.000004503549489433212,0,0,0],
		"st":{"gr":True,"as":0},
		"ti":None,
		"m":msg, #message here.
		"ci": 20764
	}
	try:
		response = requests.post(
			"https://mps.geo-fs.com/update",
			json = body,
			cookies = {"PHPSESSID": geofs_session_id}
		)
		response_body = json.loads(response.text)
		return response_body["myId"]
	except:
		print("Error code 2. Failed message sender.")

def getMessages(myId, geofs_session_id, lastMsgId):
	body = {
		"origin": "https://www.geo-fs.com",
		"acid":"707105",
		"sid":geofs_session_id,
		"id":myId,
		"ac":"1",
		"co":[42.36021568682466,-70.98767598755524,4.589746820023676,-103.04273973572526,-15.919583740307557,-0.376840533503692],
		"ve":[2.7011560632672626e-10,7.436167948071671e-11,0.000004503549489433212,0,0,0],
		"st":{"gr":True,"as":0},
		"ti":None,
		"m": "",
		"ci": lastMsgId
	}
	try:
		response = requests.post(
			"https://mps.geo-fs.com/update",
			json = body,
			cookies = {"PHPSESSID": geofs_session_id}
		)
		response_body = json.loads(response.text)
		return response_body["myId"], response_body["lastMsgId"], response_body["chatMessages"]
	except:
		print("Error code 1. Failed handshake.")