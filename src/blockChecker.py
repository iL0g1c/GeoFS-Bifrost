from guildFiles import loadGuildFile

def blockChecker(guildId, messages):
    error, guildData = loadGuildFile()
    for guild in guildData:
        if guild["id"] == guildId:
            for i in range(len(messages)):
                for accountId in guild["blockedAccounts"]:
                    if accountId == messages[i]["acid"]:
                        del messages[i]
    return messages