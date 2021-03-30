import inspect
from helper import *

if __name__ == "__main__":
    try:
        api = init()
        flwrs = api.followers()
        for flwr in flwrs:
            if flwr.following == False:
                api.create_friendship(flwr.id)
                print("Followed", str(flwr.id))
    except Exception as e:
        print("Error: " + str(e))
