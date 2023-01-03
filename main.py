import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

time = input(
    "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

url = f"https://www.billboard.com/charts/hot-100/{time}/"

response = requests.get(url)
website_data = BeautifulSoup(response.text, "html.parser")
titles = website_data.find_all(
    name="h3", class_="a-no-trucate", id="title-of-a-story")
song_names = [song.getText().strip() for song in titles]


year = time.split("-")[0]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        show_dialog=True,
        cache_path="token.txt"
    )
)

song_uris = []
user_id = sp.current_user()["id"]

for name in song_names:
    try:
        song = sp.search(q=f"track:{name} year:{year}", type="track")
        song_uris.append(song["tracks"]["items"][0]["uri"])
    except IndexError:
        continue

playlist = sp.user_playlist_create(
    user=user_id, name=f"{time} Billboard 100", public=False)
print(playlist["id"])

add_tracks = sp.user_playlist_add_tracks(
    user=user_id, playlist_id=playlist["id"], tracks=song_uris)
print(add_tracks)
