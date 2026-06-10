class Playlist:
    def __init__(self, name):
        self._name = name
        self._songs = []
        self._duration = 0

    @property
    def name(self):
        return self._name

    @property
    def duration(self):
        return self._duration

    def get_songs(self):
        return list(self._songs)

    def add_song(self, title, length):
        if length <= 0:
            raise ValueError("Song length must be positive.")
        self._songs.append((title, length))
        self._duration += length
   
    def remove_song(self, title):
        for song_title, length in self._songs:
            if song_title == title:
                self._songs.remove((song_title, length))
                self._duration -= length
                return
        raise ValueError("Song not found.")

if __name__ == "__main__":
    my_playlist = Playlist("Chill Vibes")
    
    try:
        my_playlist.add_song("Bad Song", -5)
    except ValueError as e:
        print(f"Caught expected validation error: {e}") 

    try:
        my_playlist.name = "New Name"
    except AttributeError:
        print("Success: 'name' is read-only and cannot be directly modified.")

    
    my_playlist.add_song("Good Song", 180)
    songs_copy = my_playlist.get_songs()
    songs_copy.append(("Hacked Song", 999)) 
    
    print(f"Internal duration after copy mutation: {my_playlist.duration}s") 