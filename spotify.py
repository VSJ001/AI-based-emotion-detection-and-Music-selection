from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
import spotipy.util as util
import random
class MySpotify:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.redirect_url = 'https://google.com/'
        self.auth_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        self.token = self.auth_manager.get_access_token(as_dict=True)['access_token']
        self.spotify = spotipy.Spotify(client_credentials_manager= self.auth_manager)

    def open_spotify_songs(self, emotion):
        searched_songs = self.spotify.search(q=emotion, limit=5, type="track")
        webbrowser.open(searched_songs["tracks"]["items"][random.randint(0,4)]["external_urls"]["spotify"])

    def open_spotify_playlist(self, emotion):
        if emotion == 'happy':
            webbrowser.open(random.choice(['https://open.spotify.com/playlist/37i9dQZF1DWZKuerrwoAGz','https://open.spotify.com/playlist/1llkez7kiZtBeOw5UjFlJq','https://open.spotify.com/playlist/37i9dQZF1EVJSvZp5AOML2','https://open.spotify.com/playlist/7sisx0RXg89LF3t6s020ER', 'https://open.spotify.com/playlist/37i9dQZF1DWZ72qOlbizxi', 'https://open.spotify.com/playlist/5eW9SsRKgfJPJyetdapKpc']))
        elif emotion == 'sad':
            webbrowser.open(random.choice(['https://open.spotify.com/playlist/7ABD15iASBIpPP5uJ5awvq', 'https://open.spotify.com/playlist/44tRfteJJzAmUONSiA56bQ']))
        elif emotion == 'angry':
            webbrowser.open(random.choice(['https://open.spotify.com/playlist/0jbaEzUwLTOlIOp42B5pXV', 'https://open.spotify.com/playlist/0KPEhXA3O9jHFtpd1Ix5OB', 'https://open.spotify.com/playlist/0KPEhXA3O9jHFtpd1Ix5OB']))
        elif emotion == 'surprise':
            webbrowser.open(random.choice(['https://open.spotify.com/playlist/72oczUf02H4RGoaUBC87JQ', 'https://open.spotify.com/playlist/37i9dQZF1DXdfOcg1fm0VG', 'https://open.spotify.com/playlist/37i9dQZF1DXbIeCFU20wRm']))
        elif emotion == 'disgust':
            webbrowser.open(random.choice(['https://open.spotify.com/playlist/5QhPtVfsgNJXDKNRxaaC7k', 'https://open.spotify.com/playlist/44tRfteJJzAmUONSiA56bQ']))
        elif emotion == 'fear':
            webbrowser.open(random.choice(['https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4', 'https://open.spotify.com/playlist/6EIVswdPfoE9Wac7tB6FNg', 'https://open.spotify.com/playlist/3G7SpGHYPwcxaPUk7SrytU']))
        else:
            webbrowser.open(random.choice(['https://open.spotify.com/playlist/37i9dQZF1DX5IDTimEWoTd']))


