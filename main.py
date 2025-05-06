import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import datetime
import locale

load_dotenv()

# === CONFIGURATION ===
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "playlist-modify-public"
locale.setlocale(locale.LC_TIME, 'Polish_Poland.1250')
now = datetime.datetime.now()
current_month = now.strftime('%B').capitalize()
current_year = now.strftime('%Y')
if now.month == 1:
    previous_month = 12
else:
    previous_month = now.month - 1
previous_month = datetime.date(now.year, previous_month, 1).strftime('%B').capitalize()
PLAYLIST_NAME_OLD = f"Eska Rap 2 | {previous_month} {current_year}"
PLAYLIST_NAME = f"Eska Rap 2 | {current_month} {current_year}"

# === SPOTIFY AUTHORIZATION ===
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

user_id = sp.current_user()["id"]

# === WEB SCRAPING ===
url = 'https://www.eska.pl/rap20/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

songs = []
for hit in soup.select('.single-hit'):
    title_tag = hit.select_one('.single-hit__title')
    artists_tag = hit.select('.single-hit__author')
    rank_tag = hit.select_one('.single-hit__position')

    if not title_tag or not artists_tag or not rank_tag:
        continue

    title = title_tag.text.strip()
    artists = ", ".join([a.text.strip() for a in artists_tag])
    rank = int(rank_tag.text.strip())

    songs.append({
        "rank": rank,
        "title": title,
        "artists": artists
    })

# === RANKING SORTING ===
songs = sorted(songs, key=lambda x: x["rank"])

# === SEARCH ON SPOTIFY ===
track_uris = []

for song in songs:
    query = f"{song['title']} {(song['artists'])}"
    print(query)
    result = sp.search(q=query, type="track", limit=1)
    tracks = result["tracks"]["items"]
    if tracks:
        uri = tracks[0]["uri"]
        track_uris.append(uri)
    else:
        print(f"Not found: {query}")

# === FIND OR CREATE A PLAYLIST ===
playlists = sp.current_user_playlists()
playlist_id = None

for p in playlists["items"]:
    if (p["name"] == PLAYLIST_NAME or p["name"] == PLAYLIST_NAME_OLD):
        playlist_id = p["id"]
        break
if not playlist_id:
    playlist = sp.user_playlist_create(user_id, PLAYLIST_NAME, public=True)
    playlist_id = playlist["id"]
else:
    # delete all existing songs
    current_tracks = sp.playlist_items(playlist_id)
    uris_to_remove = [item["track"]["uri"] for item in current_tracks["items"]]
    if uris_to_remove:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, uris_to_remove)

current_datetime = datetime.datetime.now().strftime('%d.%m.%Y')
playlist_description = f"Zaktualizowano dnia {current_datetime}"
playlist_name = PLAYLIST_NAME

# === ADD SONGS AND UPDATE INFO ===
if track_uris:
    sp.playlist_add_items(playlist_id, track_uris)
    sp.playlist_change_details(playlist_id, name=playlist_name, description=playlist_description)

    print("Playlist updated!")
else:
    print("Could not add any songs.")
