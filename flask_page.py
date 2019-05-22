import spotipy
from flask import Flask, request, abort, send_file, session, render_template, url_for
from spotify_token import Spotify_token



app = Flask(__name__)

app.config['SECRET_KEY'] = 'The secret key which ciphers the cookie'

@app.route("/", methods=["GET", "POST"])
def route():
    return render_template('main.html')

@app.route("/search", methods=["GET", "POST"])
def search():
    print(request)
    print(request.url)
    print(request.args)
    if request.method == "GET":
        artist = request.args.get("artist")
        query = request.args.get("query")
    else:
        res = request.form
        query = res["query"]
        artist = None
    results = spotify_search(query, artist)
    return render_template("search.html", results=results, query=query)


def spotify_search(query, ref_artist):
    result = sp.search(query, limit=50, market="JP", type="album")
    items = result["albums"]["items"]
    result_list = []
    artist_dict = {}
    for albums in items:
        result_dict = {}
        album_name = albums["name"]
        artists = albums["artists"]
        check_list = artist_check(artists)
        print(check_list, ref_artist)
        if ref_artist not in check_list and ref_artist != None:
            continue
        image = albums["images"][1]["url"]
        album_url = albums["external_urls"]["spotify"]
        result_dict["image"] = image
        result_dict["album_name"] = album_name
        result_dict["album_url"] = album_url
        artist_list = []
        for artist in artists:
            artist_name = artist["name"]
            artist_list.append(artist_name)
            if artist_name not in artist_dict:
                artist_dict[artist_name] = 1
            else:
                artist_dict[artist_name] = artist_dict[artist_name] + 1
        result_dict["artist"] = artist_list
        result_list.append(result_dict)
    sorted_list = sorted(artist_dict.items(), key=lambda x: x[1], reverse=True)
    new_dict = {}
    for sort in sorted_list:
        new_dict[sort[0]] = sort[1]
    return result_list, new_dict, query

def artist_check(artists):
    artist_list = []
    for artist in artists:
        artist_name = artist["name"]
        artist_list.append(artist_name)
    return artist_list

if __name__ == "__main__":
    username = ""  # SpotifyのユーザーID
    ST = Spotify_token(username)
    token = ST.set()
    sp = spotipy.Spotify(auth=token)
    app.run()