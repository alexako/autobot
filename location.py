import json
import urllib2
import pusher_client
from time import sleep


def get_location():
    try:
        resp = urllib2.urlopen("http://ip-api.com/json/").read()
        obj = json.loads(resp)
        payload = {
            "lat": obj["lat"],
            "lng": obj["lon"]
        }
        print payload
        pusher_client.trigger("update-gps", payload)
    except:
        print "Error"


if __name__ == '__main__':

    while True:
        get_location()
        sleep(3)
