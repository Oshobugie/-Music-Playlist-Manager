# models.py

import re
from typing import List, Optional

class Song:
    """Represents a single song."""
    def __init__(self, title: str, artist: str, album: str, duration: int, filepath: str):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration  # in seconds
        self.filepath = filepath

    def __str__(self) -> str:
        """User-friendly string representation."""
        minutes, seconds = divmod(self.duration, 60)
        return f'"{self.title}" by {self.artist} ({minutes:02d}:{seconds:02d})'

    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        return f"Song(title='{self.title}', artist='{self.artist}', filepath='{self.filepath}')"

    def __eq__(self, other) -> bool:
        """Two songs are equal if their filepaths are the same."""
        if not isinstance(other, Song):
            return NotImplemented
        return self.filepath == other.filepath

    def __hash__(self) -> int:
        """Required for making Song objects hashable (e.g., for sets)."""
        return hash(self.filepath)

class Playlist:
    """Represents a playlist of songs."""
    def __init__(self, name: str):
        self.name = name
        self.songs: List[Song] = []

    def add_song(self, song: Song):
        """Adds a song to the end of the playlist."""
        if song not in self.songs:
            self.songs.append(song)

    def remove_song(self, index: int):
        """Removes a song from the playlist by its index."""
        if 0 <= index < len(self.songs):
            self.songs.pop(index)

    def reorder_song(self, old_index: int, new_index: int):
        """Moves a song from an old index to a new index."""
        if 0 <= old_index < len(self.songs) and 0 <= new_index < len(self.songs):
            song_to_move = self.songs.pop(old_index)
            self.songs.insert(new_index, song_to_move)

    def __len__(self) -> int:
        """Returns the number of songs in the playlist."""
        return len(self.songs)

    def __getitem__(self, index: int) -> Song:
        """Allows accessing songs by index."""
        return self.songs[index]

class Library:
    """Represents the entire music library."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def search(self, query: str) -> List[Song]:
        """
        Performs a smart search on the library.
        The query is case-insensitive and can match title, artist, or album.
        """
        if not query:
            return self.songs

        results = []
        # Use regex for flexible matching, ignoring case
        try:
            pattern = re.compile(query, re.IGNORECASE)
            for song in self.songs:
                if (pattern.search(song.title) or
                    pattern.search(song.artist) or
                    pattern.search(song.album)):
                    results.append(song)
        except re.error:
            # Handle invalid regex patterns gracefully
            return []
        return results
