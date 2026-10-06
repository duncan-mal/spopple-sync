import logging
import sys
from pathlib import Path
from ytmusicapi import setup
from ytmusicapi import YTMusic
from ytmusicapi.exceptions import YTMusicError
from utils import config
from utils import err_codes as err
from utils import sqlite as sql

def get_youtube_client():

    if not Path(config.config_p.get("YouTube_Music","cache_path")).exists():
        setup(
            filepath="app/.youtube_cache",
            headers_raw=Path(config.config_p.get("YouTube_Music","header_path")).read_text(),
        )

    return YTMusic(config.config_p.get("YouTube_Music","cache_path"))

def test_youtube_client():

    get_youtube_client()

    try:

        if get_youtube_client() is not None:
            logging.info("Authenticated YouTube Music Client")
    except Exception:
        logging.critical("YouTube Authentication failed, exiting")
        sys.exit(err.YT_MUSIC_AUTHENTICATION_ERROR)

def find_single_song_id(song):
    search_term = song.get("Title") + " By " + song.get("Artist")
    logging.debug("Searching for " + search_term)
    results = get_youtube_client().search(search_term, filter="songs")

    if not results:
        logging.warning("No results for " + search_term + ", skipping")
    try:
        i=0

        while song["YoutubeID"] is None:
            song["YoutubeID"] = results[i].get("videoId")
            i+=1
        logging.debug("Found YouTube ID for " + search_term + ": " + song["YoutubeID"])
        return song
    except IndexError:
        return None

def add_song(song, playlist_id):

    response = get_youtube_client().add_playlist_items(
        playlistId=playlist_id,
        videoIds=[song["YoutubeID"]],
    )
    if response == "STATUS_SUCCEEDED":
        return True
    if response["status"] == "STATUS_FAILED":
        if response["actions"][0]["addToToastAction"]["item"]["notificationActionRenderer"]["responseText"]["runs"][0]["text"] == "This track is already in the playlist":
            logging.warning(f"{song["Title"]} by {song["Artist"]} already in playlist, ONLY adding to internal database")
            return True
    return False

def remove_song(video_obj, playlist_id):
    response = get_youtube_client().remove_playlist_items(
        playlistId=playlist_id,
        videos=[video_obj],
    )
    if response == "STATUS_SUCCEEDED":
        return True
    return False

def get_youtube_playlist(playlist_id):
    try:
        playlist = get_youtube_client().get_playlist(
            playlistId=playlist_id,
            limit=None
        )["tracks"]
        return playlist
    except (KeyError, YTMusicError):
        logging.warning(f"Could not read playlist (treating as empty)")
        return []







