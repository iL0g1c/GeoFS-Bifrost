import urllib.parse
def parseChat(messages):
    msg = ""
    for message in messages:
        message["msg"] = urllib.parse.unquote(message["msg"])
        msg += f"({message['acid']}){message['cs']}> {message['msg']}\n"
    return msg