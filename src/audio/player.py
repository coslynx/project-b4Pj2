import asyncio
import logging

import discord

from src.audio import downloader, queue

# Set up logging
logger = logging.getLogger(__name__)


class AudioPlayer:
    """
    Represents an audio player that manages audio playback for a Discord bot.

    This class handles connecting to voice channels, playing audio from various sources,
    and managing the playback queue. It interacts with the Discord API to stream audio
    to users in a voice channel.
    """

    def __init__(self):
        self._guild: Optional[discord.Guild] = (
            None  # The Discord guild this player is associated with
        )
        self._voice_client: Optional[discord.VoiceClient] = (
            None  # The Discord voice client
        )
        self._current_song: Optional[downloader.YTDLSource] = (
            None  # The currently playing song
        )
        self._queue: queue.SongQueue = (
            queue.SongQueue()
        )  # The queue of songs to be played
        self._loop = asyncio.get_event_loop()  # The event loop for asynchronous operations

    @property
    def is_playing(self) -> bool:
        """
        Checks if the audio player is currently playing audio.

        Returns:
            bool: True if audio is playing, False otherwise.
        """
        return self._voice_client is not None and self._voice_client.is_playing()

    @property
    def current_song_title(self) -> Optional[str]:
        """Returns the title of the currently playing song, or None if no song is playing."""
        return self._current_song.title if self._current_song else None

    async def connect(self, voice_channel: discord.VoiceChannel):
        """
        Connects to the specified voice channel.

        Args:
            voice_channel (discord.VoiceChannel): The voice channel to connect to.
        """
        if self._voice_client is not None:
            await self._voice_client.move_to(voice_channel)
        else:
            self._voice_client = await voice_channel.connect()
        self._guild = voice_channel.guild

    async def disconnect(self):
        """
        Disconnects from the current voice channel if connected.
        """
        if self._voice_client is not None and self._voice_client.is_connected():
            await self._voice_client.disconnect()
            self._voice_client = None
            self._guild = None

    async def play(self, source: downloader.YTDLSource):
        """
        Starts playing the provided audio source.

        Args:
            source (downloader.YTDLSource): The audio source to play.
        """
        if self._voice_client is not None:
            logger.info(f"Playing song: {source.title}")
            self._current_song = source
            self._voice_client.play(
                source,
                after=lambda e: self._loop.create_task(self._play_next()),
            )

    def pause(self):
        """
        Pauses the current audio playback.
        """
        if self._voice_client is not None and self._voice_client.is_playing():
            self._voice_client.pause()

    def resume(self):
        """
        Resumes the paused audio playback.
        """
        if self._voice_client is not None and self._voice_client.is_paused():
            self._voice_client.resume()

    async def stop(self):
        """
        Stops the current audio playback and clears the queue.
        """
        if self._voice_client is not None:
            self._voice_client.stop()
            self._current_song = None
            self._queue.clear()

    async def skip(self):
        """
        Skips to the next song in the queue.
        """
        await self._play_next()

    async def _play_next(self):
        """
        Plays the next song in the queue.
        This method is intended to be called internally and is not part of the public API.
        """
        if self._voice_client is not None:
            next_song = await self._queue.play_next()
            if next_song:
                await self.play(next_song)
            else:
                logger.info("Playback queue is empty.")
                self._current_song = None

    async def enqueue(self, song: downloader.YTDLSource):
        """
        Adds a song to the playback queue.

        Args:
            song (downloader.YTDLSource): The song to add to the queue.
        """
        await self._queue.enqueue(song)
        if not self.is_playing:
            await self._play_next()

    def get_queue(self):
        """
        Retrieves the current playback queue.

        Returns:
            queue.SongQueue: The current song queue.
        """
        return self._queue