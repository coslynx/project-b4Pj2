import discord
from discord.ext import commands
from src.audio import player


class General(commands.Cog):
    """
    General commands for the bot.
    """

    def __init__(self, bot: commands.Bot, audio_player: player.AudioPlayer):
        self.bot = bot
        self.audio_player = audio_player

    @commands.command(name="ping", help="Check the bot's latency.")
    async def ping(self, ctx: commands.Context):
        """
        Responds with the bot's latency.
        """
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! Latency: {latency}ms")

    @commands.command(name="join", help="Make the bot join your voice channel.")
    async def join(self, ctx: commands.Context):
        """
        Connects the bot to the user's voice channel.
        """
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            await self.audio_player.connect(voice_channel)
            await ctx.send(f"Connected to {voice_channel.name}")
        else:
            await ctx.send("You are not connected to a voice channel.")

    @commands.command(name="leave", help="Make the bot leave the voice channel.")
    async def leave(self, ctx: commands.Context):
        """
        Disconnects the bot from the voice channel.
        """
        if self.audio_player._voice_client and self.audio_player._voice_client.is_connected():
            await self.audio_player.disconnect()
            await ctx.send("Disconnected from voice channel.")
        else:
            await ctx.send("Not connected to any voice channel.")

    @commands.command(name="help", help="Show this help message.")
    async def help(self, ctx: commands.Context):
        """
        Displays the help message with available commands.
        """
        help_text = "**Available Commands:**\n\n"
        for cog in self.bot.cogs:
            help_text += f"**{cog}:**\n"
            for command in self.bot.get_cog(cog).get_commands():
                help_text += f"`{self.bot.command_prefix}{command.name}`: {command.help}\n"
            help_text += "\n"
        await ctx.send(help_text)


async def setup(bot: commands.Bot):
    """
    Loads the General cog.
    """
    await bot.add_cog(General(bot, bot.audio_player))