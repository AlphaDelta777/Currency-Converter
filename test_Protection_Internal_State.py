
from Protection_Internal_State import Playlist  

def test_name_and_duration_are_readonly():
    """Verify that directly modifying properties raises an AttributeError."""
    playlist = Playlist("Indie Rock")
    
    try:
        playlist.name = "New Name"
        assert False, "Encapsulation failed: 'name' attribute is modifiable!"
    except AttributeError:
        pass  

    try:
        playlist.duration = 500
        assert False, "Encapsulation failed: 'duration' attribute is modifiable!"
    except AttributeError:
        pass  


def test_validation_prevents_negative_length():
    """Verify that negative or zero-length songs throw a ValueError."""
    playlist = Playlist("Indie Rock")
    
    try:
        playlist.add_song("Broken Track", -5)
        assert False, "Validation failed: Allowed negative song length!"
    except ValueError:
        pass


def test_get_songs_returns_immutable_copy():
    """Verify that mutating the returned list doesn't affect internal state."""
    playlist = Playlist("Indie Rock")
    playlist.add_song("Float On", 208)
    
    songs_copy = playlist.get_songs()
    songs_copy.append(("Hacked Song", 999))
    
    assert len(playlist.get_songs()) == 1, "Bonus failed: Internal list was mutated!"
    assert playlist.duration == 208, "Invariant failed: Internal duration changed!"


def test_remove_song_maintains_duration():
    """Verify that removing a song properly updates the duration invariant."""
    playlist = Playlist("Indie Rock")
    playlist.add_song("Float On", 208)
    
    playlist.remove_song("Float On")
    assert playlist.duration == 0, "Duration was not decremented correctly!"
    assert len(playlist.get_songs()) == 0, "Song was not removed from list!"