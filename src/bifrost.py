import os
from dotenv import load_dotenv
import discord
from discord.ext import tasks, commands
import time
from multiplayer_api import init_server_instance, getMessages, sendMsg
from chat import parseChat
from guildFiles import loadGuildFile, saveGuildFile
from data import saveData, loadData
from spamChecker import spamCheck
from blockChecker import blockChecker
from errors import getErrors

intents = discord.Intents.all()
load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
geofs_session_id = os.getenv("GEOFS_SESSION_ID")
bot = commands.Bot(intents=intents, command_prefix="bf! ")

CATALOG_DIR = "catalog/"


def setup():
	if not os.path.exists(CATALOG_DIR):
		os.mkdir(CATALOG_DIR)
	if not os.path.exists(CATALOG_DIR + "guilds.jsonl"):
		with open(CATALOG_DIR + "guilds.jsonl", "w") as fp:
			pass
	if not os.path.exists(CATALOG_DIR + "data.json"):
		with open(CATALOG_DIR + "data.json", "w") as fp:
			fp.write("{}")

	guildData = loadGuildFile()[1]
	for i in range(len(guildData)):
		if "blockedAccounts" not in guildData[i]:
			guildData[i]["blockedAccounts"] = []
	saveGuildFile(guildData)


@tasks.loop(seconds=1)
async def printMessages(bot):
	errorCode, data = loadData()
	if errorCode:
		raise getErrors(errorCode)

	myId, lastMsgId, messages = getMessages(data["myId"], geofs_session_id, data["lastMsgId"])
	data["lastMsgId"] = lastMsgId
	data["myId"] = myId
	saveData(data)

	errorCode, guildData = loadGuildFile()
	if errorCode:
		raise getErrors(errorCode)

	for i in range(len(guildData)):
		if guildData[i]["chatTrackerEnabled"]:
			errorCode, blockCheckedMessages = blockChecker(guildData[i]["id"], messages)
			if errorCode:
				raise getErrors(errorCode)

			msg = parseChat(blockCheckedMessages)

			channel = bot.get_channel(guildData[i]["chatTrackerChannel"])
			if msg != "":
				await channel.send(discord.utils.escape_markdown(msg))

@bot.event
async def on_ready():
	errorCode, data = loadData()
	if errorCode:
		raise getErrors(errorCode)

	data["myId"], data["lastMsgId"] = init_server_instance(geofs_session_id, returnMyId=True)
	saveData(data)
	print("Bot has connected to discord.")
	printMessages.start(bot)

@bot.event
async def on_guild_join(guild):
	inDatabase = False
	print(f"OspreyEyes has been added to {guild.id}.\n Setting up...")

	errorCode, guildData = loadGuildFile()
	if errorCode:
		raise getErrors(errorCode)

	for obj in guildData:
		if obj["id"] == guild.id:
			inDatabase = True

	if not inDatabase:
		guildData.append({
			"id": guild.id,
			"chatTrackerChannel": None,
			"chatTrackerEnabled": False,
			"lastMessage": None,
			"lastMessageTime": time.time(),
			"blockedAccounts": [],

		})
	saveGuildFile(guildData)
	print("Setup successful.")

@bot.command(brief="Check connection.", description="Check connection.")
async def ping(ctx):
	delay = round(bot.latency * 1000)
	await ctx.send(f"PONG!\n {delay}ms")

@bot.command(brief="Set callsign tracker channel.", description="Set callsign tracker channel.")
async def setChannel(ctx, channel):
	isChannelValid = False
	if isinstance(accountID, int):
		isChannelValid = True
		accountID = int(accountID)
	if not isChannelValid:
		errorMessage = getErrors(5)
		await ctx.send(errorMessage)
	errorCode, guildData = loadGuildFile()
	if errorCode:
		errorMessage = getErrors(errorCode)
		await ctx.send(errorMessage)
		return

	for i in range(len(guildData)):
		if guildData[i]["id"] == ctx.message.guild.id:
			guildData[i]["chatTrackerChannel"] = int(channel)
			await ctx.send(f"Binded chat transcription to channel id: {channel}")
	saveGuildFile(guildData)

@bot.command(brief="Toggle chat tracker on and off.", description="Toggle chat tracker on and off.")
async def toggleChat(ctx):
	await ctx.send("Toggling tracking...")

	errorCode, guildData = loadGuildFile()
	if errorCode:
		errorMessage = getErrors(errorCode)
		await ctx.send(errorMessage)
		return

	for i in range(len(guildData)):
		if guildData[i]["id"] == ctx.message.guild.id:
			if guildData[i]["chatTrackerEnabled"]:
				guildData[i]["chatTrackerEnabled"] = False
				await ctx.send("Tracking terminated.")
			else:
				guildData[i]["chatTrackerEnabled"] = True
				await ctx.send("Tracking started.")
	saveGuildFile(guildData)

@bot.command(brief="Say something in GeoFS chat.", description="Say something in GeoFS chat.")
async def say(ctx, message):
	errorCode, data = loadData()
	if errorCode:
		errorMessage = getErrors(errorCode)
		await ctx.send(errorMessage)
		return

	parsedMessage = f"{ctx.message.author.name} | {message}"
	errorCode, isSpam, spamResponse = spamCheck(ctx, message)
	if errorCode:
		errorMessage = getErrors(errorCode)
		await ctx.send(errorMessage)
		return

	if isSpam:
		await ctx.send(spamResponse)
	else:
		myId = sendMsg(data["myId"], parsedMessage, geofs_session_id)
		data["myId"] = myId
	saveData(data)

@bot.command(brief="A debugging command that outputs in console instead of GeoFS.", description="A debugging command that outputs in console instead of GeoFS.")
async def consoleSay(ctx, message):
	errorCode, data = loadData()
	if errorCode:
		errorMessage = getErrors(errorCode)
		await ctx.send(errorMessage)
		return

	parsedMessage = f"{ctx.message.author.name} | {message}"
	errorCode, isSpam, spamResponse = spamCheck(ctx, message)
	if errorCode:
		errorMessage = getErrors(errorCode)
		await ctx.send(errorMessage)
		return

	if isSpam:
		print(f"**SPAM DETECTED: {spamResponse}**")
	else:
		print(parsedMessage)
	saveData(data)
	
@bot.command(brief="Block a user from your message stream with the account ID.", description="Block a user from your message stream with the account ID.")
async def block(ctx, accountID):
	if isinstance(accountID, int):
		accountID = int(accountID)
	else:
		errorMessage = getErrors(3)
		await ctx.send(errorMessage)

	errorCode, guildData = loadGuildFile()
	if errorCode:
		errorMessage = getErrors(errorCode)
		await ctx.send(errorMessage)
		return

	for i in range(len(guildData)):
		if guildData[i]["id"] == ctx.message.guild.id:
			guildData[i]["blockedAccounts"].append(accountID)
	saveGuildFile(guildData)
	await ctx.send(f"Blocked account: {accountID}")

@bot.command(brief="Unblock a user from your message stream with the account ID.", description="Unblock a user from your message stream with the account ID.")
async def unblock(ctx, accountID):
	if isinstance(accountID, int):
		accountID = int(accountID)
	else:
		errorMessage = getErrors(3)
		await ctx.send(errorMessage)

	errorCode, guildData = loadGuildFile()
	if errorCode:
		errorMessage = getErrors(errorCode)
		await ctx.send(errorMessage)
		return

	for i in range(len(guildData)):
		if guildData[i]["id"] == ctx.message.guild.id:
			for j in range(len(guildData[i]["blockedAccounts"])):
				if guildData[i]["blockedAccounts"][j] == accountID:
					del guildData[i]["blockedAccounts"][j]
	saveGuildFile(guildData)
	await ctx.send(f"Unblocked account: {accountID}")
	
@bot.command(brief="View your servers block list.", description="View your servers block list.")
async def blocklist(ctx):
	isAnyUserBlocked = False
	msg = "Here are your current blocked AccountIDs:\n"

	errorCode, guildData = loadGuildFile()
	if errorCode:
		errorMessage = getErrors(errorCode)
		await ctx.send(errorMessage)
		return

	for guild in guildData:
		if guild["id"] == ctx.message.guild.id:
			for i in range(len(guild["blockedAccounts"])):
				isAnyUserBlocked = True
				msg += f"{i+1}. {guild['blockedAccounts'][i]}\n"
			break
	if not isAnyUserBlocked:
		msg = getErrors(1)
	await ctx.send(msg)

if __name__ in "__main__":
	setup()
	bot.run(BOT_TOKEN)
