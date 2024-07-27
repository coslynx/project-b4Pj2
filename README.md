# Discord Music Bot

This is a Python-based Discord music bot that allows users to play music from YouTube and Spotify within their Discord servers. The bot offers features like queue management, playback controls, playlist support (future), and more.

## Features

* **Music Playback:**
    * Join and leave voice channels on user request.
    * Stream music from YouTube and Spotify.
    * Support for multiple audio formats (MP3, FLAC, WAV, etc.).
* **Queue Management:**
    * Add songs to the playback queue.
    * View the current queue with song titles and durations.
    * Remove songs from the queue.
    * Clear the entire queue.
* **Playback Controls:**
    * Play, pause, resume, and stop music playback.
    * Skip to the next or previous song in the queue.
    * Loop the current song or the entire queue.
    * Adjust the volume of the music playback.
* **User Experience:**
    * Intuitive and easy-to-use commands for interaction.
    * Clear and informative error messages for troubleshooting.
    * Embed messages with song information and queue details.
* **Additional Features (Future Expansion):**
    * Playlist support: Create, save, and load playlists.
    * User preferences: Store user-specific volume and playback settings.
    * Advanced search: Search for music by artist, album, or lyrics.
    * Lyrics display: Fetch and display lyrics for the currently playing song.
    * Radio integration: Stream music from online radio stations.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/discord-music-bot.git
   cd discord-music-bot
   ```
2. **Set up a virtual environment (recommended):**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure the bot:**
   * Create a `.env` file in the project root based on the `.env.example` file.
   * Replace the placeholders in `.env` with your actual Discord bot token, Spotify client ID, and Spotify client secret.
5. **Run the bot:**
   ```bash
   python src/main.py
   ```

## Usage

1. Invite the bot to your Discord server.
2. Join a voice channel.
3. Use the bot's commands to play music, manage the queue, and control playback.

**Basic Commands:**

* `!play <song title or link>`: Play a song.
* `!pause`: Pause the current song.
* `!resume`: Resume playback.
* `!stop`: Stop playback and clear the queue.
* `!skip`: Skip to the next song.
* `!queue`: View the current queue.
* `!clear`: Clear the queue.
* `!join`: Make the bot join your voice channel.
* `!leave`: Make the bot leave the voice channel.

**Note:** Command prefix may vary. Refer to the bot's help command for a full list of commands and their usage.

## Contributing

Contributions are welcome! Please open an issue or pull request if you have any suggestions, bug reports, or feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.