import asyncio
import logging

import youtube_dl
import discord

from src.utils import helpers

# Set up logging
logger = logging.getLogger(__name__)


class YTDLSource(discord.PCMVolumeTransformer):
    """
    This class handles downloading and preparing audio from YouTube.
    It uses youtube-dl to fetch audio streams and provides methods to control playback.
    """

    def __init__(self, source, *, data, volume=0.5):
        """
        Initializes the YTDLSource object.

        Args:
            source (discord.AudioSource): The underlying audio source.
            data (dict): Information about the audio track.
            volume (float, optional): Initial volume level (0.0 to 1.0). Defaults to 0.5.
        """
        super().__init__(source, volume)

        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")
        self.duration = data.get("duration")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        """
        Creates a YTDLSource object from a given URL.

        Args:
            url (str): The URL of the audio source.
            loop (asyncio.event_loop, optional): The event loop to use.
            stream (bool, optional): Whether to stream the audio. Defaults to False.

        Returns:
            YTDLSource: A YTDLSource object representing the audio source, or None if an error occurs.
        """
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: cls.extract_info(url, download=not stream)
        )
        if data is None:
            logger.error(f"Failed to extract audio info for URL: {url}")
            return None

        filename = data["url"] if stream else data["filepath"]
        try:
            source = discord.FFmpegPCMAudio(filename, **helpers.ffmpeg_options)
            return cls(source, data=data)
        except Exception as e:
            logger.error(f"Failed to create audio source: {e}")
            return None

    @staticmethod
    def extract_info(url, *, download=True):
        """
        Extracts information about the audio source from the given URL using youtube-dl.

        Args:
            url (str): The URL of the audio source.
            download (bool, optional): Whether to download the audio. Defaults to True.

        Returns:
            dict: A dictionary containing information about the audio source, or None if an error occurs.
        """
        with youtube_dl.YoutubeDL(helpers.ytdl_options) as ydl:
            try:
                info = ydl.extract_info(url, download=download)
                if "entries" in info:
                    info = info["entries"][0]  # Get the first video if it's a playlist
                return info
            except (
                youtube_dl.utils.DownloadError,
                youtube_dl.utils.ExtractorError,
            ) as e:
                logger.error(f"Error downloading audio: {e}")
                return None