
def getErrors(errorCode):
    if errorCode == 1:
        return "Your server has no blocked users."
    elif errorCode == 2:
        return "Internal Server Error: 'guilds.jsonl' does not exist.\n Please contact OspreyEyes."
    elif errorCode == 3:
        return "Incorrect value for the Account ID parameter."
    elif errorCode == 4:
        return "Internal Server Error: 'data.json' does not exist.\n Please contact OspreyEyes."
    elif errorCode == 5:
        return "Incorrect value for the Account ID parameter."
    elif errorCode == 6:
        return "You have not set your display name with the 'setNick' command, so you can't type in chat."