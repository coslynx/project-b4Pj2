import asyncio
import discord
from discord.ext import commands
from src.audio import downloader, player


class Music(commands.Cog):
    """Music-related commands."""

    def __init__(self, bot: commands.Bot, audio_player: player.AudioPlayer):
        self.bot = bot
        self.audio_player = audio_player

    @commands.command(name="play", help="Play a song from YouTube or Spotify.")
    async def play(self, ctx: commands.Context, *, query: str):
        """Plays a song based on the provided query.

        Args:
            ctx (commands.Context): The context of the command invocation.
            query (str): The search query or URL for the song.
        """

        if not ctx.author.voice:
            return await ctx.send("You are not connected to a voice channel.")

        voice_channel = ctx.author.voice.channel
        if self.audio_player._guild != ctx.guild:
            await self.audio_player.connect(voice_channel)

        async with ctx.typing():
            try:
                source = await downloader.YTDLSource.from_url(
                    query, loop=self.bot.loop, stream=True
                )
            except Exception as e:
                return await ctx.send(
                    f"An error occurred while processing your request: {e}"
                )

            if source is None:
                return await ctx.send(
                    "Could not find a suitable audio source. Please check your query and try again."
                )

            await self.audio_player.enqueue(source)
            await ctx.send(f"Added to queue: {source.title}")

    @commands.command(name="pause", help="Pause the current song.")
    async def pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""
        if self.audio_player.is_playing:
            self.audio_player.pause()
            await ctx.send("Paused the music.")
        else:
            await ctx.send("No music is currently playing.")

    @commands.command(name="resume", help="Resume paused music.")
    async def resume(self, ctx: commands.Context):
        """Resumes a paused song."""
        if not self.audio_player.is_playing:
            self.audio_player.resume()
            await ctx.send("Resumed the music.")
        else:
            await ctx.send("Music is already playing.")

    @commands.command(name="stop", help="Stop playing music and clear the queue.")
    async def stop(self, ctx: commands.Context):
        """Stops the current playback and clears the queue."""
        await self.audio_player.stop()
        await ctx.send("Stopped playing music and cleared the queue.")

    @commands.command(name="skip", help="Skip to the next song in the queue.")
    async def skip(self, ctx: commands.Context):
        """Skips the currently playing song."""
        if self.audio_player.is_playing:
            await self.audio_player.skip()
            await ctx.send("Skipped to the next song.")
        else:
            await ctx.send("No music is currently playing to skip.")

    @commands.command(name="queue", help="Show the current music queue.")
    async def queue(self, ctx: commands.Context):
        """Displays the current song queue."""
        queue_items = self.audio_player.get_queue().get_queue()
        if not queue_items:
            return await ctx.send("The queue is empty.")

        queue_text = "**Music Queue:**\n"
        for i, song in enumerate(queue_items, start=1):
            queue_text += f"{i}. {song.title} ({song.duration:.2f}s)\n"
        await ctx.send(queue_text)

    @commands.command(name="clear", help="Clear the music queue.")
    async def clear(self, ctx: commands.Context):
        """Clears the song queue."""
        self.audio_player.get_queue().clear()
        await ctx.send("Cleared the queue.")


async def setup(bot: commands.Bot):
    """Adds the Music cog to the bot."""
    await bot.add_cog(Music(bot, bot.audio_player))