import os
import discord
from discord.ext import commands
from src.audio import player, queue
from src.utils import helpers
from src.config import settings

# Load environment variables if available
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set.")

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.members = True  # For fetching member information

bot = commands.Bot(command_prefix=settings.COMMAND_PREFIX, intents=intents)

# Initialize the shared audio player and queue
audio_player = player.AudioPlayer()
music_queue = queue.MusicQueue()

# Load and register bot commands and event listeners
# (assuming you have separate files for these)
bot.load_extension("src.commands.music")
bot.load_extension("src.commands.general")
bot.load_extension("src.events.bot_events")

@bot.event
async def on_ready():
    """Event handler for when the bot connects to Discord."""
    print(f"Logged in as {bot.user.name}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="your commands!"
        )
    )
    await helpers.load_commands(bot)

# Error handling for CommandNotFound
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Use `!help` for a list of commands.")
    else:
        print(f"An error occurred: {error}")
        await ctx.send(
            "An error occurred while processing your request. Please try again later."
        )

# Start the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)