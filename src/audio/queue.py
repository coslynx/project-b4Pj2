import asyncio
from typing import List, Optional

from src.audio import downloader


class SongQueue:
    """Represents a queue of songs to be played."""

    def __init__(self):
        self._queue: List[downloader.YTDLSource] = []
        self._loop = asyncio.get_event_loop()
        self._current_song: Optional[downloader.YTDLSource] = None

    @property
    def current_song(self) -> Optional[downloader.YTDLSource]:
        """Returns the currently playing song."""
        return self._current_song

    @property
    def is_empty(self) -> bool:
        """Checks if the queue is empty."""
        return not self._queue

    async def enqueue(self, song: downloader.YTDLSource):
        """Adds a song to the end of the queue."""
        self._queue.append(song)

    def dequeue(self) -> Optional[downloader.YTDLSource]:
        """Removes and returns the song at the front of the queue."""
        if self.is_empty:
            return None
        return self._queue.pop(0)

    async def play_next(self):
        """Plays the next song in the queue."""
        if self._current_song:
            self._current_song.cleanup()
            self._current_song = None

        if self.is_empty:
            return

        self._current_song = self.dequeue()
        if self._current_song:
            return self._current_song
        else:
            return None  # Queue became empty while switching

    def clear(self):
        """Clears the entire queue."""
        self._queue.clear()
        if self._current_song:
            self._current_song.cleanup()
            self._current_song = None

    def get_queue(self) -> List[downloader.YTDLSource]:
        """Returns a copy of the current queue."""
        return self._queue.copy()