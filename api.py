from time import sleep
import flask
import RPi.GPIO as GPIO
from motor import Motor


app = flask.Flask(__name__)
app.config["DEBUG"] = True


def setup_gpio():
    """ Setup GPIO Pins """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LEFT1, GPIO.OUT)
    GPIO.setup(LEFT2, GPIO.OUT)
    GPIO.setup(RIGHT1, GPIO.OUT)
    GPIO.setup(RIGHT2, GPIO.OUT)


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
    motor.forward()
    sleep(0.25)
    motor.neutral()
    return "Moved forward"

@app.route("/reverse", methods=["GET"])
def reverse():
    """ Move bot backward """
    motor.reverse()
    sleep(0.25)
    motor.neutral()
    return "Moved backward"

@app.route("/left", methods=["GET"])
def turn_left():
    """ Turn bot left """
    motor.left()
    sleep(0.25)
    motor.neutral()
    return "Turned left"

@app.route("/right", methods=["GET"])
def turn_right():
    """ Turn bot right """
    motor.right()
    sleep(0.25)
    motor.neutral()
    return "Turned right"

@app.route("/activate", methods=["GET"])
def activate():
    """ Activate autobot """
    toggle_green()
    return "Autobot on"

@app.route("/deactivate", methods=["GET"])
def deactivate():
    """ Deactivate auto """
    toggle_red()
    return "Autobot off"


if __name__ == '__main__':

    LED_G = 11
    LED_R = 7

    # Motors
    LEFT1 = 31
    LEFT2 = 33
    RIGHT1 = 35
    RIGHT2 = 37

    motor = Motor(LEFT1, LEFT2, RIGHT1, RIGHT2)
    setup_gpio()

    try:
        toggle_green()
        toggle_red()
        app.run(host='0.0.0.0', port=3000)
    except KeyboardInterrupt:
        GPIO.cleanup()
