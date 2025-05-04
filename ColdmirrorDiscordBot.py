# Importing libraries and modules
import os # Allows interaction with the operating system
import discord # Provides methods to interact with the Discord API
from discord.ext import commands # Extends discord.py and allows creation and handling of commands
from discord import app_commands # Allows parameters to be used for slash-commands
from dotenv import load_dotenv # Allows the use of environment variables (this is what we'll use to manage our
                               # tokens and keys)
import asyncio
from collections import deque
import json
import random

from keep_alive import keep_alive

# Environment variables for tokens and other sensitive data
load_dotenv() # Loads and reads the .env file
TOKEN = os.getenv("DISCORD_TOKEN") # Reads and stores the Discord Token from the .env file

keep_alive()

# Define the allowed channel ID (replace with your actual bot-test channel ID)
ALLOWED_CHANNEL_IDS = [1353078571085594745, 1353120270138867753, 1368682440499007560]

# Setup of intents. Intents are permissions the bot has on the server
intents = discord.Intents.default() # Intents can be set through this object
intents.message_content = True  # This intent allows you to read and handle messages from users

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents) # Creates a bot and uses the intents created earlier

# Bot ready-up code
@bot.event # Decorator
async def on_ready():
    await bot.tree.sync() # Syncs the commands with Discord so that they can be displayed
    print(f"{bot.user} is online!") # Appears when the bot comes online

# Funktion zum Laden der Zitate aus der Datei
def load_quotes():
    with open("coldmirror_quotes.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Restrict message event to the allowed channel
@bot.event
async def on_message(msg):
    if msg.author == bot.user or msg.channel.id not in ALLOWED_CHANNEL_IDS:
        return
    if msg.channel.id == 1368682440499007560:
        await msg.channel.send('Interesting message!')
    await bot.process_commands(msg)

# Restrict slash command to the allowed channel
@bot.tree.command(name='coldmirror_quote', description='Sends a random Coldmirror quote')
async def coldmirror_quote(interaction: discord.Interaction):
    if interaction.channel.id not in ALLOWED_CHANNEL_IDS:
        await interaction.response.send_message("This command can only be used in specific channels!", ephemeral=True)
        return
    
    quotes = load_quotes()
    random_quote = random.choice(quotes)  # Zufälliges Zitat auswählen
    quote_text = f'**"{random_quote["quote"]}"**\n📌 *{random_quote["source"]}*'

    # Falls ein Link existiert, füge ihn mit <> hinzu
    if "link" in random_quote and random_quote["link"]:
        quote_text += f'\n <{random_quote["link"]}>'

    await interaction.response.send_message(quote_text)


# Run the bot
bot.run(TOKEN) # This code uses your bot's token to run the bot
