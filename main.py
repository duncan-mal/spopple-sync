import sys
import time
from pathlib import Path
import logging
from services import spotify_client as sc
from services import youtube_client as yc
from utils import sqlite as sql
from utils import config

def main():
    # Logging Setup
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s | %(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info("SpoppleSync started")
    #Check for config file's existence, read if exists
    if not Path("app/config.ini").is_file():
        logging.warning("Config file not found, creating")
        config.make_config()
        config.config_p.read("app/config.ini")
    else:
        logging.info("Config file found, reading config")
        config.config_p.read("app/config.ini")

    #Add File Handler to logger
    file_handler = logging.FileHandler(config.config_p.get("Service", "log_path"), "w")
    file_handler.setFormatter(logging.Formatter("[%(asctime)s | %(levelname)s] %(message)s"))
    logging.getLogger().addHandler(file_handler)



    #Test client connections
    sc.test_spotify_client()
    yc.test_youtube_client()

    #Main Loop
    try:
        while True:
            start  = time.monotonic()
            ##Beginning of main loop
            logging.info("Running playlist sync")

            add_count = 0

            spotify_playlist = sc.get_spotify_playlist(config.config_p.get("Spotify", "playlist_id")) #get songs from Spotify
            youtube_playlist = yc.get_youtube_playlist(config.config_p.get("YouTube_Music", "playlist_id")) #get song dicts from YouTube

            #Add missing songs
            for song in spotify_playlist:
                if not sql.check_for_song(song):
                    add_count += 1
                    sql.add_song(song)
            if add_count > 0:
                logging.info(f"Added {add_count} songs to playlist")
            else:
                logging.info("No songs added to playlist")

            remove_count = sql.trim_extra(spotify_playlist, youtube_playlist) #trims extra and returns number removed

            if remove_count > 0:
                logging.info(f"Removed {remove_count} songs from playlist")
            else:
                logging.info("No songs removed from playlist")

            logging.info("Finished playlist sync successfully")
            ##End of main loop
            elapsed = time.monotonic() - start
            time.sleep(max(0, int(config.config_p.get("Service","loop_seconds"))-elapsed))
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt, exiting")

main()