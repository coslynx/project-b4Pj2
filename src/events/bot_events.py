import discord
from discord.ext import commands
from src.audio import player


class BotEvents(commands.Cog):
    """Handles bot events."""

    def __init__(self, bot: commands.Bot, audio_player: player.AudioPlayer):
        self.bot = bot
        self.audio_player = audio_player

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        """
        Event listener for when a member's voice state changes.

        This method checks if the bot is alone in a voice channel and disconnects if it is.
        It also handles pausing and resuming playback if the bot is the only other member.

        Args:
            member (discord.Member): The member whose voice state changed.
            before (discord.VoiceState): The member's previous voice state.
            after (discord.VoiceState): The member's current voice state.
        """
        if (
            self.audio_player._voice_client
            and self.audio_player._voice_client.is_connected()
        ):
            voice_channel = self.audio_player._voice_client.channel
            if len(voice_channel.members) == 1:
                # Bot is alone in the voice channel, disconnect
                await self.audio_player.disconnect()
            elif (
                len(voice_channel.members) == 2
                and voice_channel.members[0].id == self.bot.user.id
            ):
                # Bot is the only other member in the voice channel
                if after.channel is None:
                    # User left, pause playback
                    self.audio_player.pause()
                elif before.channel is None:
                    # User joined, resume playback
                    self.audio_player.resume()


async def setup(bot: commands.Bot):
    """Loads the BotEvents cog."""
    await bot.add_cog(BotEvents(bot, bot.audio_player))