import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
import utils.err_codes as err
from utils import config


def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=config.config_p.get("Spotify", "client_id"),
        client_secret=config.config_p.get("Spotify", "client_secret"),
        redirect_uri=config.config_p.get("Spotify", "redirect_uri"),
        scope=config.config_p.get("Spotify", "scope"),
        open_browser=False,
        cache_path=config.config_p.get("Spotify", "cache_path"),
    ))

def get_spotify_playlist(playlist_id):
    songs = []
    client = get_spotify_client()
    results = client.playlist_tracks(playlist_id)

    if results:
        logging.info(f"Found playlist {results.get("name")}")
    else:
        logging.error(f"Could not find playlist with ID {config.config_p.get("Spotify", "playlist_id")}")
        return None

    while results:
        for song in results["items"]:
            track = song["item"]
            if track is None:
                continue

            if track.get("external_ids",{}).get("isrc") is None:
                logging.warning(f"Song {track.get("name")} by {track.get("artists",{})[0].get("name")} has no ISRC")
                continue

            songs.append(
                {
                    "ISRC":track.get("external_ids",{}).get("isrc"),
                    "Title":track.get("name"),
                    "Artist":track.get("artists",{})[0].get("name"),
                    "YoutubeID":None
                }
            )
        results = client.next(results)
    logging.info(f"Found {len(songs)} Spotify songs")

    return songs

def test_spotify_client():
    spotify = get_spotify_client()
    user = spotify.current_user()
    if user is None:
        logging.critical("Failed to authenticate spotify user")
        sys.exit(err.SPOTIFY_AUTHENTICATION_ERROR)
    else:
        logging.info(f"Authenticated Spotify User : {user['display_name']}")
