import ssl
import spotipy
import threading
import subprocess

from pathlib import Path
from pytubefix import Search
from pytubefix import YouTube
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


class Downloader:
    def __init__(self):
        load_dotenv()
        ssl._create_default_https_context = ssl._create_stdlib_context

        self.download_dir = "downloads"
        self.naming_ndx = 0

        auth_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def pull_spotify_playlist_tracks(self, link):
        trackRequest = self.sp.playlist_tracks(
            link,
            fields="items.track.artists.name,items.track.name",
            additional_types="track",
        )["items"]

        trackInfo = []
        for i in trackRequest:
            s = i["track"]["artists"][0]["name"] + " - " + i["track"]["name"]
            trackInfo.append(s)

        return trackInfo

    def get_youtube_url_by_name(self, name):
        return Search(name).videos[0].watch_url

    def mp3_to_raw(self, folder_path, set_label, on_finish):
        input_dir = Path(folder_path)
        output_dir = Path(folder_path + "_raw")
        output_dir.mkdir(exist_ok=True)

        def convert_thread():
            for mp3_file in input_dir.glob("*.mp3"):
                raw_file = output_dir / (mp3_file.stem + ".raw")

                cmd = [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(mp3_file),
                    "-f",
                    "s16le",
                    "-acodec",
                    "pcm_s16le",
                    "-ac",
                    "2",
                    "-ar",
                    "44100",
                    str(raw_file),
                ]

                set_label(f"Converting {mp3_file.name} -> {raw_file.name}")
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

            set_label("✅ All conversions complete.")
            on_finish()

        thread = threading.Thread(target=convert_thread, daemon=True)
        thread.start()

    def download_audio_mp3(self, link, name):
        filename = ""
        if not (self.indexing):
            filename = name
        else:
            filename = f"{self.naming_ndx}"

        YouTube(link).streams.get_audio_only().download(
            output_path=self.download_dir,
            filename=f"{filename}.mp3",
        )

    def start_download(
        self,
        url,
        dir,
        set_label,
        on_download_finished,
        on_track_downloaded,
        indexing,
        start,
        end,
    ):
        self.download_dir = dir
        self.indexing = indexing

        def download_thread():
            try:
                tracks = self.pull_spotify_playlist_tracks(url)
            except:
                set_label("Link is not correct.")
                on_download_finished()
                return

            if start > len(tracks) or end > len(tracks):
                on_download_finished()
                set_label("Playlist doesn't have that many songs!")
                return

            for i in range(start - 1, end):
                trackName = tracks[i]
                try:
                    videoURL = self.get_youtube_url_by_name(trackName)
                    self.download_audio_mp3(videoURL, trackName)

                    set_label("Downloaded: " + trackName)
                    on_track_downloaded(str(i) + ") " + trackName)

                    self.naming_ndx += 1
                except:
                    on_track_downloaded(str(i) + ") (Error) " + trackName)
                    set_label("An error occured during: " + trackName)

            on_download_finished()
            set_label("Download Complete ✔️")
            self.naming_ndx = 0

        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
