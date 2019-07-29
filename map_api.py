from time import sleep
import urllib2
import os
import json
from flask import Flask, render_template, url_for, request
import pusher_client


# Globals
app = Flask(__name__, template_folder="template")
app.config["DEBUG"] = True

# Routes
@app.route("/", methods=["GET"])
def home():
    """ Render docs page """
    return render_template("map.html")

@app.route("/directions", methods=["POST"])
def directions():
    data = request.form
    print data
    origin = data.get("origin")
    destination = data.get("destination")
    url = """\
            https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&key=%s
        """ % (origin, destination, os.environ["GOOGLE_MAPS_API_KEY"]);
    return str(urllib2.urlopen(url).read()) 

@app.route("/payload", methods=["POST"])
def autodeploy():
    """ Autodeploy webhook """
    os.system("git pull")
    return "Done"

@app.route("/stream", methods=["GET"])
def stream():
    """ Render docs page """
    return render_template("stream.html")

@app.route("/update-location", methods=["POST"])
def update_location():
    """ Update clients with latest GPS coords (FORM) """
    print request.form
    payload = {
        "lat": request.form.get("latitude"),
        "lng": request.form.get("longitude")
    }
    pusher_client.trigger("update-gps", payload)
    return json.dumps(payload)

@app.route("/update-gps", methods=["POST"])
def update_gps():
    """ Update clients with latest GPS coords """
    data = request.get_json()
    print data
    payload = {
        "lat": data["latitude"],
        "lng": data["longitude"]
    }
    pusher_client.trigger("update-gps", payload)
    return json.dumps(payload)


if __name__ == '__main__':

    try:
        app.run(host='0.0.0.0', port=3000)
        pusher_client.trigger("api-status", "Online")
    except KeyboardInterrupt:
        GPIO.cleanup()
