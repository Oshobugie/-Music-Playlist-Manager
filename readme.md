# Music Playlist Manager - by Group 14

This project is a simple music playlist manager built with Python and tkinter. It allows users to manage playlists from a local/mock song library.

## Features (MVP)

-   **Search**: Search a library of songs by title, artist, or album.
-   **Build Playlists**: Add songs from the library to a playlist.
-   **Reorder**: Change the order of tracks in the playlist.
-   **Export**: Save the playlist to a standard `.m3u` file.

## How to Run

1.  Make sure you have Python 3 installed.
2.  Run the main application file:
    ```bash
    python app.py
    ```
3.  To run the unit tests:
    ```bash
    python -m unittest test_playlist.py
    ```

## Project Structure

-   `app.py`: The main application entry point and UI (using tkinter).
-   `models.py`: Contains the `Song`, `Playlist`, and `Library` data classes.
-   `utils.py`: Helper functions, such as for exporting to M3U format.
-   `mock_data.py`: A mock dataset of songs to populate the library.
-   `test_playlist.py`: Unit tests for the playlist functionality.
