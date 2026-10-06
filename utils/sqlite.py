import logging
import sqlite3 as sql
from pathlib import Path
from utils.config import config_p
import services.youtube_client as yc

def get_database():
    db_exists = Path(config_p.get("Service", "db_path")).exists()
    conn = sql.connect(config_p.get("Service","db_path"))
    conn.row_factory = sql.Row
    if not db_exists:
        logging.warning("SQLite database not found, creating...")
        conn.execute(
        """
        CREATE TABLE IF NOT EXISTS songs (
        isrc                   TEXT PRIMARY KEY,
        name                   TEXT,
        artist                 TEXT,
        youtube_id             TEXT
        )
        """
        )
    return conn

def check_for_song(song):
    conn = get_database()
    isrc = song.get("ISRC")

    cur = conn.execute("SELECT isrc FROM songs WHERE isrc = ?", (isrc,))



    if cur.fetchone() is not None:
        logging.debug(f"Found {song.get("Title")} by {song.get("Artist")} in database")
        return True
    else:
        logging.debug(f"Didnt find {song.get("Title")} by {song.get("Artist")} in database")
        return False

def add_song(song):
    conn = get_database()
    song = yc.find_single_song_id(song)

    if yc.add_song(song, config_p.get("YouTube_Music","playlist_id")):
        if song is None:
            return

        try:
            conn.execute(
            """
            INSERT INTO songs (isrc, name, artist, youtube_id)
            VALUES (?, ?, ?, ?)
            """,
            (song.get("ISRC"), song.get("Title"), song.get("Artist"), song.get("YoutubeID"))
                               )
            conn.commit()
        finally:
            conn.close()
    else:
        logging.warning(f"Failed to add song: {song["Title"]} by {song["Artist"]}")

def remove_song(isrc):
    conn = get_database()
    try:
        conn.execute("""
        DELETE FROM songs WHERE isrc = ?
        """,
        (isrc,)
                    )
        conn.commit()
    finally:
        conn.close()

def trim_extra(spotify_playlist, youtube_playlist):
    conn = get_database()
    spotify_ids = []
    extras = []
    for song in spotify_playlist:
        spotify_ids.append(song.get("ISRC"))

    db_rows = conn.execute("SELECT isrc, youtube_id FROM songs").fetchall()

    for row in db_rows:
        if not spotify_ids.__contains__(row["isrc"]):
            yt_track = next((t for t in youtube_playlist if t.get("videoId") == row["youtube_id"]), None)
            if yt_track is not None:
                if yc.remove_song(yt_track, config_p.get("YouTube_Music","playlist_id")):
                    extras.append(row["isrc"])
                else:
                    logging.warning(f"Failed to remove song: {row["Title"]} by {row["artist"]}")



    for isrc in extras:
        remove_song(isrc)

    return len(extras)

def get_song(isrc):
    conn = get_database()
    cur = conn.execute("SELECT * FROM songs WHERE isrc = ?", (isrc,))
    return cur.fetchone()







