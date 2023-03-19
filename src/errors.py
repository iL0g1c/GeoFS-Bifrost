
def getErrors(errorCode):
    match errorCode:
        case 1:
            return "Your server has no blocked users."
        case 2:
            return "Internal Server Error: 'guilds.jsonl' does not exist.\n Please contact OspreyEyes."
        case 3:
            return "Incorrect value for the Account ID parameter."
        case 4:
            return "Internal Server Error: 'data.json' does not exist.\n Please contact OspreyEyes."
        case 5:
            return "Incorrect value for the Account ID parameter."