import os
import tweepy
import requests
from dotenv import load_dotenv

load_dotenv()


def init():
    auth = tweepy.OAuthHandler(
        os.environ.get("TWITTER_API_KEY"),
        os.environ.get("TWITTER_API_SECRET")
    )
    auth.set_access_token(
        os.environ.get("TWITTER_ACCESS_KEY"),
        os.environ.get("TWITTER_ACCESS_SECRET")
    )
    return tweepy.API(auth)


def get_station(query: str) -> str or None:
    aqicn_key = os.environ.get("AQICN_TOKEN")
    response = requests.get(
        f"https://api.waqi.info/search/?token={aqicn_key}&keyword={query}"
    )
    if (len(response.json()['data']) > 0):
        return response.json()['data'][0]['uid']
    return


def get_station_data(uid: str) -> dict or None:
    aqicn_key = os.environ.get("AQICN_TOKEN")
    response = requests.get(
        f"https://api.waqi.info/feed/@{uid}/?token={aqicn_key}"
    )
    if response.json()['data'] == "Unknown station":
        return
    return response.json()['data']
