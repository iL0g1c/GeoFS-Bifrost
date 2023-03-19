import time
from guildFiles import loadGuildFile, saveGuildFile

def spamCheck(ctx, message):
    isSpam = False
    errorCode, guildData = loadGuildFile()
    if errorCode:
        return errorCode, None, None

    spamResponse = ""
    for i in range(len(guildData)):
        if guildData[i]["id"] == ctx.guild.id:
            if guildData[i]["lastMessage"] == message:
                isSpam = True
                spamResponse = "You can't say the same thing twice."
            if time.time() - guildData[i]["lastMessageTime"] < 3:
                isSpam = True
                spamResponse = "Your server can only send a message every three seconds."
            guildData[i]["lastMessage"] = message
            guildData[i]["lastMessageTime"] = time.time()
            break
    saveGuildFile(guildData)
    return None, isSpam, spamResponse