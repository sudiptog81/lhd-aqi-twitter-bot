import tweepy
import inspect
from helper import *

api = None


class AQIStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            qry = ''
            twt = status.text.split()
            api.create_favorite(status.id)

            if twt[0] == "@AQITwtBot":
                qry = ' '.join(twt[1:])
            else:
                if str(status.user.screen_name).lower() != 'aqitwtbot':
                    api.update_status(
                        status=inspect.cleandoc(
                            f"""
                            Reply to this tweet with <city name> or Tweet @AQITwtBot <city name> to get the latest #AQI updates!
                            """
                        ),
                        in_reply_to_status_id=status.id,
                        auto_populate_reply_metadata=True
                    )
                    return

            if (qry):
                stn = get_station(qry)
                data = get_station_data(stn)

                if data == "Unknown station":
                    api.update_status(
                        status=inspect.cleandoc(
                            f"""
                            Oops! An air quality monitoring station was not found for that place. Try again with a different place maybe! #AQI
                            """
                        ),
                        in_reply_to_status_id=status.id,
                        auto_populate_reply_metadata=True
                    )
                    return

                twt = api.update_status(
                    status=inspect.cleandoc(
                        f"""
                        #AQI @ {data['city']['name']} is {data['aqi']} as on {data['time']['iso']} #Automation #AQITwtBot
                        Source: World Air Quality Index Project
                        """
                    ),
                    in_reply_to_status_id=status.id,
                    auto_populate_reply_metadata=True
                )
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    try:
        api = init()
        stream_listener = AQIStreamListener()
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        print("Listening for mentions of @AQITwtBot")
        stream.filter(track=['AQITwtBot'])
    except Exception as e:
        print("Error:", str(e))
