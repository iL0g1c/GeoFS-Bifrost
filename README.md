# GeoFS-Bifrost
## What is Bifrost
BiFrost is a discord bot that allows communication between GeoFS chat and discord servers by connecting the two via a bridge.

## How to setup Bifrost
1. Add the bot to your server using this link:
   - ```https://discord.com/api/oauth2/authorize?client_id=1086763337230073936&permissions=67110912&scope=bot```
   - These are the minimum requirements for the bot to work, and may be updated in the future.
     - Currently the bot only needs "Send Messages" to work.
2. If you wish to use the bot in a private channel, you will need to add the bot's role "Project Bifrost" to the channels you wish to use it in.
3. You can check your connection with ```bf! ping```
4. In order to receive GeoFS chat messages in your server you must use ```bf! setChannel [Channel ID]```
   - Replace "[Channel ID]" with the channel id of the channel you want the message stream to be in.
5. To activate the message stream use ```bf! toggleChat```
6. In order to talk in GeoFS chat you must use: ```bf! say [message]```
   - **Multiword messages must be in double quotes.**

## Censorship
### Spam
To prevent users from weaponizing Bifrost for spamming GeoFS chat, there is a spam filter.
Your message will be block if you meet one or both of these conditions:
1. Your discord server tries to send the same message twice in a row.
2. Your discord server tries to send multiple messages within three seconds.

Currently the spam filter is applied at the server's scope, but this may change.

### Blocking GeoFS Accounts
This feature has yet to be implemented, but it will allow servers to block accounts that they do not wish to see in their message stream.
Each server will have their own block list.
A user will be blocked using ```bf! block [Account ID]```
