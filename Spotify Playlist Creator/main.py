from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import requests
import os

user = os.environ.get("SPOTIPY_CLIENT_ID")
secret = os.environ.get("SPOTIPY_CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=user,
        client_secret=secret,
        show_dialog=True,
        cache_path="token.txt",
    )
)

user_id = sp.current_user()["id"]


def main():
    # Ask the user which date they want the spotify playlist to reflect
    music_date = input(
        "Which year do you want to travel to? Type the date in this format: YYYY-MM-DD: "
    )

    # Web scrap billboard.com to see what the top 100 songs were on that date
    response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{music_date}/")
    music_data = response.text

    # Use BeautifulSoup to create a searchable format
    soup = BeautifulSoup(music_data, "html.parser")

    # Isolate the track names of the top 100 songs
    titles = soup.select("li ul li h3")
    title_list = [title.getText().strip() for title in titles]

    # Using a for loop, search spotify for the track name and add the song link path to a list
    spotify_track_list = []

    for song in title_list:
        result = sp.search(song, limit=1, offset=0, type="track", market=None)
        try:
            spotify_id = result["tracks"]["items"][0]["uri"]
            spotify_track_list.append(spotify_id)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")

    # Create a new playlist on the users Spotify account
    playlist = sp.user_playlist_create(
        user=user_id, name=f"test {music_date}", public=False, description="no idea"
    )

    # Add all the songs from Spotify track list to the new Spotify playlist
    sp.playlist_add_items(playlist_id=playlist["id"], items=spotify_track_list)


if __name__ == "__main__":
    main()

