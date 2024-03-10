import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# To access authorised Spotify data
client_id = "# your client id"
client_secret = "your client secret"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artist = "Moses Sumney"
track = "Lonely World"

track_id = sp.search(q="artist:" + artist + " track:" + track, type="track")
trackId = track_id["tracks"]["items"][0]["id"] # retrives spotify track id from the name given
print(trackId)


''' Spotify Shortcuts '''
# Quick Search : ctrl + k
# Shuffle : ctrl + s