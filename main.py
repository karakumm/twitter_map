'''
Module for creating map with twitter friend's locations.
'''
import json
import requests
import folium
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable
from flask import Flask, render_template, request

geolocator = Nominatim(user_agent="karakum")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def users_info(username: str, bearer_token: str):
    '''
    Returns information about twitter friends.
    '''
    url = "https://api.twitter.com/"

    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    parameters = {
        'screen_name': f'@{username}',
        'count': 15
    }

    find_url = f'{url}1.1/friends/list.json'

    response = requests.get(find_url, headers=headers, params=parameters)

    response_json = response.json()['users']


    info_result = []
    for profile in response_json:
        user_info = [profile['name'], profile['location']]
        info_result.append(user_info)

    return info_result


def get_coords(users_data):
    '''
    Gets latitude and longtitude of twitter friends' locations.
    '''
    locations_lst = []
    for user in users_data:
        try:
            location = geolocator.geocode(user[1])
            user.append(location.latitude)
            user.append(location.longitude)
            locations_lst.append(user)
        except: GeocoderUnavailable
    return locations_lst


def create_map(users_coords):
    '''
    Creates map with twitter friends' locations
    '''
    latitude = 49.043005102937286
    longtitude = 24.36109362474663
    loc = [latitude, longtitude]
    map = folium.Map(location= loc,
                    zoom_start=100)

    fg = folium.FeatureGroup(name="Nearest film's locations")
    for loc in users_coords:
        fg.add_child(folium.Marker(location=[loc[2], loc[3]],
                            popup=loc[0],
                            icon=folium.Icon()))
        map.add_child(fg)

    map.save('map.html')


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create_map", methods=["POST"])
def twitter_map():
    name = request.form.get("name")
    token = request.form.get("bearer_token")
    if not name or not token:
        return render_template("failure.html")
    create_map(get_coords(users_info(name, token)))
    return render_template("twitter_map.html")

if __name__ == "__main__":
    app.run(debug=False)


