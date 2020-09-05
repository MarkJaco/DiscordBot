from discord.ext import commands
import handle_message
import time


client = commands.Bot(command_prefix='.')
BOT_ID = 751529287605289072
messageHandler = handle_message.MessageHandler(BOT_ID)
current_poll = None


# ready
@client.event
async def on_ready():
    print("Bot is ready.")


# every message
@client.event
async def on_message(message):
    global current_poll
    await messageHandler.handle_message(message)

client.run('NzUxNTI5Mjg3NjA1Mjg5MDcy.X1KaMA.VKtxeTMK8bI3jC4s-PLsRf84y70')