from time import sleep
import flask
import RPi.GPIO as GPIO


app = flask.Flask(__name__)
app.config["DEBUG"] = True


def setup_gpio():
    """ Setup GPIO Pins """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_R, GPIO.OUT)


def toggle_green():
    """ Toggle green LED """
    GPIO.output(LED_G, True)
    sleep(0.5)
    GPIO.output(LED_G, False)

def toggle_red():
    """ Toggle red LED """
    GPIO.output(LED_R, True)
    sleep(0.5)
    GPIO.output(LED_R, False)

@app.route("/", methods=["GET"])
def home():
    """ Render docs page """
    return "Autobot API"

@app.route("/forward", methods=["GET"])
def forward():
    """ Move bot forward """
    return "Moved forward"

@app.route("/left", methods=["GET"])
def turn_left():
    """ Turn bot left """
    toggle_green()
    return "Turned left"

@app.route("/right", methods=["GET"])
def turn_right():
    """ Turn bot right """
    toggle_red()
    return "Turned right"

@app.route("/activate", methods=["GET"])
def turn_right():
    """ Turn bot right """
    toggle_green()
    return "Turned right"

@app.route("/deactivate", methods=["GET"])
def turn_right():
    """ Turn bot right """
    toggle_red()
    return "Turned right"


if __name__ == '__main__':

    LED_G = 11
    LED_R = 7

    setup_gpio()

    try:
        toggle_green()
        toggle_red()
        app.run(host='0.0.0.0', port=3000)
    except KeyboardInterrupt:
        GPIO.cleanup()
