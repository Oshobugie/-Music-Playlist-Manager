# utils.py

from models import Playlist

def export_to_m3u(playlist: Playlist, filename: str):
    """
    Exports a playlist to an M3U file.
    M3U is a simple format with one file path per line.
    """
    if not filename.lower().endswith('.m3u'):
        filename += '.m3u'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for song in playlist.songs:
            # #EXTINF is a common extension that includes duration and title
            f.write(f"#EXTINF:{song.duration},{song.artist} - {song.title}\n")
            f.write(f"{song.filepath}\n")
    print(f"Playlist '{playlist.name}' exported to '{filename}'")

