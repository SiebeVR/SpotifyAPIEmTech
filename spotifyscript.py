import requests, json
import base64
from columnar import columnar
from requests.api import get


authurl = "https://accounts.spotify.com/api/token"
authheader = {}
authdata = {}


def getAccessToken(clientID, clientSecret):
    
    message = clientID + ":" + clientSecret
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    
    authheader["Authorization"] = "Basic " + base64_message
    authdata["grant_type"] = "client_credentials"
    url_response = requests.post(authurl, headers=authheader, data=authdata)

    if url_response.status_code != 200:
        return None
    else:
        url_data = url_response.json()
        access_token = url_data["access_token"]
        return access_token



def getPlaylistTracks(access_token, playlistID):
    playlistEndpoint = "https://api.spotify.com/v1/playlists/" + playlistID
    getHeader = {"Authorization": "Bearer " + access_token}
    url_request = requests.get(playlistEndpoint, headers=getHeader)
    url_data = url_request.json()
    return url_data


##ClientID = input("Geef je Spotify Client ID:  ")
##ClientSecret = input("Geef je Spotify Client Secret:  ")
ClientID = "95775b3b4c9f4c7b95c1aa0d589c25bf"
ClientSecret = "df83a796ba7248cf86f002b05a7e4ccd"
access_token = getAccessToken(ClientID, ClientSecret)



if not access_token:
    print("Authenticatie mislukt!")
else:
    playlist_url = input("Geef hier de playlist url (Geef 'stop' of 'exit' in om het programma te stoppen):  ")
    while playlist_url:
        if playlist_url.lower() in ["stop", "exit"]:
            playlist_url = False
        else:
            
            check_playlist_url = playlist_url.find("https://open.spotify.com/playlist/")
            if check_playlist_url == -1:
                print("Afspeellijst niet gevonden! \n")
                playlist_url = input("Geef hier de playlist url (Geef 'stop' of 'exit' in om het programma te stoppen):  ")
            else:
                playlistID = playlist_url.lstrip("https://open.spotify.com/playlist/")
                trackList = getPlaylistTracks(access_token, playlistID)
                headers = ["NUMMER", "TITEL", "ARTIEST", "ALBUM", "DUUR"]
                track_counter = 0
                data = []

                for track in trackList["tracks"]["items"]:
                    track_counter += 1
                    song_name = track["track"]["name"].capitalize()
                    artist_name = track["track"]["artists"][0]["name"].capitalize()
                    album_name = track["track"]["album"]["name"].capitalize()
                    time = track["track"]["duration_ms"]
                    time_min = (int(time) / 1000) / 60
                    current_data = [track_counter, song_name, artist_name, album_name, "{:.2f}".format(time_min) + " min"]
                    data.append(current_data)

                table = columnar(data, headers, no_borders=False)
                print(table)
                print()
                playlist_url = input("Geef hier de playlist url (Geef 'stop' of 'exit' in om het programma te stoppen):  ")
