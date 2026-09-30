import sys
import configparser
import logging
import utils.err_codes as err


config_p = configparser.ConfigParser()

def make_config():
    try:
        with open("app/config.ini", "x") as config:
            config.write("""
[Spotify]
client_id = 
client_secret =
playlist_id = 
;Dont touch these unless you know what you're doing
redirect_uri = http://127.0.0.1:8888/callback
scope = playlist-read-private playlist-read-collaborative
cache_path = app/.spotify_cache
                         
[YouTube_Music]
playlist_id = 
header_path = app/.youtube_header.txt
;Dont touch this unless you know what you're doing
cache_path = app/.youtube_music_cache
                         
[Service]
loop_seconds = 30
log_path = app/logs/recent.log
db_path = app/app.db
                         """)
            logging.info("Config file created, modify the values accordingly")
            logging.info("Exiting")
            sys.exit(err.SYS_EXIT)
    except FileExistsError:
        logging.error("Config file already exists, canceling creation")
        config_p.read("app/config.ini")



