import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

auth_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager=auth_manager)

def search_playlists_by_mood(mood):
    query = f"{mood} mood"
    results = sp.search(q=query, type="playlist", limit=5)

    playlists = []
    for item in results["playlists"]["items"]:
        if item is None:
            continue

        name = item.get("name")
        id = item.get("id")
        url = item.get("external_urls", {}).get("spotify")
   
        images = item.get("images")
        image_url = images[0]["url"] if images and len(images) > 0 else None

        playlists.append({
            "name": name,
            "id": id,
            "url": url,
            "image": image_url
        })

    return playlists