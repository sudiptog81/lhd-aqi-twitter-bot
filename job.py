import inspect
from helper import *

if __name__ == "__main__":
    try:
        api = init()
        stn = get_station('delhi, us embassy')
        data = get_station_data(stn)
        if data == "Unknown station":
            raise Exception("Station not found")
        twt = api.update_status(
            status=inspect.cleandoc(
                f"""
                #AQI @ {data['city']['name']} is {data['aqi']} as on {data['time']['iso']} #AQIAutomationBot
                Source: World Air Quality Index Project
                """
            ),
            lat=data['city']['geo'][0],
            long=data['city']['geo'][1],
            display_coordinates=True,
            auto_populate_reply_metadata=True
        )
        print("Tweeted " + str(twt.id))
    except Exception as e:
        print("Error: " + str(e))
