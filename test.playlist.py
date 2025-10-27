# test_playlist.py

import unittest
from models import Song, Playlist

class TestPlaylistReordering(unittest.TestCase):

    def setUp(self):
        """Set up a playlist with a few songs for each test."""
        self.playlist = Playlist("My Test Playlist")
        self.song1 = Song("Song A", "Artist 1", "Album X", 180, "/path/a.mp3")
        self.song2 = Song("Song B", "Artist 2", "Album Y", 200, "/path/b.mp3")
        self.song3 = Song("Song C", "Artist 1", "Album Z", 220, "/path/c.mp3")
        self.song4 = Song("Song D", "Artist 3", "Album X", 240, "/path/d.mp3")

        self.playlist.add_song(self.song1)
        self.playlist.add_song(self.song2)
        self.playlist.add_song(self.song3)
        self.playlist.add_song(self.song4)
        # Initial order: [song1, song2, song3, song4]

    def test_move_song_down(self):
        """Test moving a song from a lower index to a higher index."""
        self.playlist.reorder_song(old_index=0, new_index=2)
        expected_order = [self.song2, self.song3, self.song1, self.song4]
        self.assertEqual([s.title for s in self.playlist.songs], [s.title for s in expected_order])

    def test_move_song_up(self):
        """Test moving a song from a higher index to a lower index."""
        self.playlist.reorder_song(old_index=3, new_index=0)
        expected_order = [self.song4, self.song1, self.song2, self.song3]
        self.assertEqual([s.title for s in self.playlist.songs], [s.title for s in expected_order])

    def test_move_to_same_index(self):
        """Test moving a song to its current position, which should not change the order."""
        initial_order = list(self.playlist.songs)
        self.playlist.reorder_song(old_index=1, new_index=1)
        self.assertEqual([s.title for s in self.playlist.songs], [s.title for s in initial_order])

    def test_move_to_end(self):
        """Test moving a song to the very end of the playlist."""
        self.playlist.reorder_song(old_index=0, new_index=3)
        expected_order = [self.song2, self.song3, self.song4, self.song1]
        self.assertEqual([s.title for s in self.playlist.songs], [s.title for s in expected_order])

    def test_invalid_indices(self):
        """Test that reordering with out-of-bounds indices does not change the playlist."""
        initial_order = list(self.playlist.songs)
        # Test with negative index
        self.playlist.reorder_song(old_index=-1, new_index=2)
        self.assertEqual(self.playlist.songs, initial_order)
        # Test with index larger than list size
        self.playlist.reorder_song(old_index=0, new_index=10)
        self.assertEqual(self.playlist.songs, initial_order)

if __name__ == '__main__':
    unittest.main()
