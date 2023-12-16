import os
import jsonlines

CATALOG_DIR = "catalog/"

def loadUserFile(guildID):
	if not os.path.exists(f"{CATALOG_DIR}{guildID}.jsonl"):
		with open(f"{CATALOG_DIR}{guildID}.jsonl", "w") as fp:
			pass
	userData = []
	with jsonlines.open(f"{CATALOG_DIR}{guildID}.jsonl") as reader:
		for obj in reader:
			userData.append(obj)
	return None, userData


def saveUserFile(guildID, userData):
    with jsonlines.open(f"{CATALOG_DIR}{guildID}.jsonl", mode='w') as writer:
        for user in userData:
            writer.write(user)

def getUserName(accountID, guildID):
	userRegistered = False
	errorCode, userData = loadUserFile(guildID)
	if errorCode:
		return errorCode, None
	if userData != []:
		for i in range(len(userData)):
			if userData[i]["userID"] == accountID:
				userRegistered = True
				break
	if not userRegistered:
		return 6, None
	return None, userData[i]["nickname"]
		