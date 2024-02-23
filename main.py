import requests

def fetch_collaborative_songs(artist_name, offset=0):
    url = f'https://musicbrainz.org/ws/2/recording?fmt=json&query=artist:"{artist_name}" OR recording:"{artist_name} feat. "%20OR%20"feat. {artist_name}"&inc=artist-rels+release-rels&offset={offset}'
    response = requests.get(url)
    data = response.json()
    
    recordings_with_official_release = [recording for recording in data.get('recordings', []) if has_official_release(recording)]
    
    return recordings_with_official_release

# Function to check if a recording has an official release
def has_official_release(recording):
    for release in recording.get('releases', []):
        if release.get('status', '').lower() == 'official':
            return True
    return False

def print_unique_collaborative_artists(collaborative_songs, artist_name):
    unique_artists = set()

    for song in collaborative_songs:
        artists = [collaborator.get('name', 'Unknown') for collaborator in song.get('artist-credit', [])]

        if len(artists) > 1 or (len(artists) == 1 and artists[0].lower() != artist_name.lower()):
            for a in artists:
                if artist_name.lower() not in a.lower() and artists.count(a) == 1:
                    unique_artists.add(a.lower())

    return list(unique_artists)

if __name__ == "__main__":
    # Specify the artist for whom you want to find collaborations * EXAMPLE *
    artist_name = "Dominic Fike"

    offset = 0
    collaborative_artists = set()

    while True:
        collaborative_songs = fetch_collaborative_songs(artist_name, offset)

        if not collaborative_songs:
            break

        collaborative_artists.update(print_unique_collaborative_artists(collaborative_songs, artist_name))

        offset += len(collaborative_songs)

    print(f"Unique artists {artist_name} has collaborated with:")
    for artist in collaborative_artists:
        print(artist.capitalize())
