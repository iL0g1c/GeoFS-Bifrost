from guildFiles import loadGuildFile

def blockChecker(guildId, oldMessages):
    errorCode, guildData = loadGuildFile()
    if errorCode:
        return errorCode, None

    newMessages = oldMessages
    for guild in guildData:
        if guild["id"] == guildId:
            for i in range(len(oldMessages)):
                for accountId in guild["blockedAccounts"]:
                    if accountId == oldMessages[i]["acid"]:
                        del newMessages[i]
    return None, newMessages