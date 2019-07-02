import RPi.GPIO as GPIO
import flask
from time import sleep


app = flask.Flask(__name__)
app.config["DEBUG"] = True


def setupGPIO():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_R, GPIO.OUT)


def toggleGreen():
    GPIO.output(LED_G, True)
    sleep(0.5)
    GPIO.output(LED_G, False)

def toggleRed():
    GPIO.output(LED_R, True)
    sleep(0.5)
    GPIO.output(LED_R, False)

@app.route("/", methods=["GET"])
def home():
    return "Autobot API"

@app.route("/forward", methods=["GET"])
def forward():
    return "Moved forward"

@app.route("/left", methods=["GET"])
def turn_left():
    toggleGreen()
    return "Turned left"

@app.route("/right", methods=["GET"])
def turn_right():
    toggleRed()
    return "Turned right"


if __name__ == '__main__':

    LED_G = 11
    LED_R = 7

    setupGPIO()

    try:
        toggleGreen()
        toggleRed()
        app.run(host='0.0.0.0', port=3000)
    except KeyboardInterrupt:
        GPIO.cleanup()
