# app.py

import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

from models import Library, Playlist
from mock import MOCK_SONGS
from utils import export_to_m3u

class PlaylistApp(tk.Tk):
    def __init__(self, library: Library):
        super().__init__()
        self.library = library
        self.playlist = Playlist(name="My Playlist")

        self.title("Music Playlist Manager")
        self.geometry("800x600")

        # --- Main Layout ---
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # --- Library Pane (Left) ---
        library_frame = tk.LabelFrame(main_frame, text="Music Library")
        library_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        library_frame.grid_rowconfigure(1, weight=1)
        library_frame.grid_columnconfigure(0, weight=1)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.update_library_list())
        search_entry = tk.Entry(library_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.library_listbox = tk.Listbox(library_frame)
        self.library_listbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
        self.library_listbox.bind("<Double-1>", self.add_song_to_playlist)

        # --- Playlist Pane (Right) ---
        playlist_frame = tk.LabelFrame(main_frame, text="Current Playlist")
        playlist_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        playlist_frame.grid_rowconfigure(0, weight=1)
        playlist_frame.grid_columnconfigure(0, weight=1)

        self.playlist_listbox = tk.Listbox(playlist_frame)
        self.playlist_listbox.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # --- Control Buttons ---
        controls_frame = tk.Frame(main_frame)
        controls_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        add_button = tk.Button(controls_frame, text="Add to Playlist ->", command=self.add_song_to_playlist)
        add_button.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(controls_frame, text="Remove from Playlist", command=self.remove_song_from_playlist)
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # Reordering buttons
        up_button = tk.Button(controls_frame, text="Move Up", command=self.move_song_up)
        up_button.pack(side=tk.LEFT, padx=5)
        
        down_button = tk.Button(controls_frame, text="Move Down", command=self.move_song_down)
        down_button.pack(side=tk.LEFT, padx=5)

        export_button = tk.Button(controls_frame, text="Export Playlist (.m3u)", command=self.export_playlist)
        export_button.pack(side=tk.RIGHT, padx=5)

        # --- Initial Population ---
        self.update_library_list()
        self.update_playlist_list()

    def update_library_list(self):
        """Updates the library listbox based on the search query."""
        search_query = self.search_var.get()
        self.library_listbox.delete(0, tk.END)
        self.songs_in_view = self.library.search(search_query)
        for song in self.songs_in_view:
            self.library_listbox.insert(tk.END, str(song))

    def update_playlist_list(self):
        """Updates the playlist listbox with the current songs."""
        self.playlist_listbox.delete(0, tk.END)
        for song in self.playlist.songs:
            self.playlist_listbox.insert(tk.END, str(song))

    def add_song_to_playlist(self, event=None):
        """Adds the selected song from the library to the playlist."""
        selected_indices = self.library_listbox.curselection()
        if not selected_indices:
            return
        selected_index = selected_indices[0]
        song_to_add = self.songs_in_view[selected_index]
        self.playlist.add_song(song_to_add)
        self.update_playlist_list()

    def remove_song_from_playlist(self):
        """Removes the selected song from the playlist."""
        selected_indices = self.playlist_listbox.curselection()
        if not selected_indices:
            return
        selected_index = selected_indices[0]
        self.playlist.remove_song(selected_index)
        self.update_playlist_list()
        # Keep selection after removal if possible
        if self.playlist.songs:
            new_selection = min(selected_index, len(self.playlist.songs) - 1)
            self.playlist_listbox.select_set(new_selection)

    def move_song_up(self):
        """Moves the selected song up in the playlist."""
        selected_indices = self.playlist_listbox.curselection()
        if not selected_indices:
            return
        old_index = selected_indices[0]
        if old_index > 0:
            new_index = old_index - 1
            self.playlist.reorder_song(old_index, new_index)
            self.update_playlist_list()
            self.playlist_listbox.select_set(new_index)

    def move_song_down(self):
        """Moves the selected song down in the playlist."""
        selected_indices = self.playlist_listbox.curselection()
        if not selected_indices:
            return
        old_index = selected_indices[0]
        if old_index < len(self.playlist.songs) - 1:
            new_index = old_index + 1
            self.playlist.reorder_song(old_index, new_index)
            self.update_playlist_list()
            self.playlist_listbox.select_set(new_index)

    def export_playlist(self):
        """Exports the current playlist to an M3U file."""
        if not self.playlist.songs:
            messagebox.showwarning("Empty Playlist", "Cannot export an empty playlist.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".m3u",
            filetypes=[("M3U Playlist", "*.m3u"), ("All Files", "*.*")],
            title="Export Playlist As"
        )
        if filename:
            export_to_m3u(self.playlist, filename)
            messagebox.showinfo("Export Successful", f"Playlist exported to {filename}")

if __name__ == "__main__":
    music_library = Library(songs=MOCK_SONGS)
    app = PlaylistApp(library=music_library)
    app.mainloop()
