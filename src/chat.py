import urllib.parse
def parseChat(messages):
    msg = ""
    for message in messages:
        message["msg"] = urllib.parse.unquote(message["msg"])
        msg += f"{message['cs']}> {message['msg']}\n"
    return msg