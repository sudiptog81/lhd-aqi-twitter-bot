import os
import tweepy
import requests
from dotenv import load_dotenv

load_dotenv()

auth = tweepy.OAuthHandler(
    os.environ.get("TWITTER_API_KEY"),
    os.environ.get("TWITTER_API_SECRET")
)
auth.set_access_token(
    os.environ.get("TWITTER_ACCESS_KEY"),
    os.environ.get("TWITTER_ACCESS_SECRET")
)

api = tweepy.API(auth)


def get_station(query: str) -> str:
    aqicn_key = os.environ.get("AQICN_TOKEN")
    response = requests.get(
        f"https://api.waqi.info/search/?token={aqicn_key}&keyword={query}"
    )
    if (len(response.json()['data']) > 0):
        return response.json()['data'][0]['uid']
    return


def get_station_data(uid: str) -> dict:
    aqicn_key = os.environ.get("AQICN_TOKEN")
    response = requests.get(
        f"https://api.waqi.info/feed/@{uid}/?token={aqicn_key}"
    )
    return response.json()['data']


class AQIStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        query = ' '.join(status.text.split()[1:])
        stn = get_station(query)
        if (stn == None):
            api.update_status(
                status=f"No station found for \"{query}\"",
                in_reply_to_status_id=status.id,
                auto_populate_reply_metadata=True
            )
            return
        data = get_station_data(stn)
        api.update_status(
            status=f"AQI for {data['city']['name']}: {data['aqi']}",
            in_reply_to_status_id=status.id,
            auto_populate_reply_metadata=True
        )
        return


aqi_stream_listener = AQIStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=aqi_stream_listener)
stream.filter(track=['#AQIAutomationBot'])
