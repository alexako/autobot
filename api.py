from time import sleep
import threading
import flask
import RPi.GPIO as GPIO
import pusher_client
import soundsensor
from collision import Collision
from motor import Motor


def setup_gpio():
    """ Setup GPIO Pins """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LEFT1, GPIO.OUT)
    GPIO.setup(LEFT2, GPIO.OUT)
    GPIO.setup(RIGHT1, GPIO.OUT)
    GPIO.setup(RIGHT2, GPIO.OUT)

def start_drive(direction):
    directions = {
        "FORWARD": motor.forward(),
        "REVERSE": motor.reverse(),
        "LEFT": motor.left(),
        "RIGHT": motor.right()
    }
    if direction in directions:
        toggle_green()
        directions[direction]
        sleep(0.25)
    else:
        collision.start()
        collision.drive(30)
        toggle_green()
        toggle_red()

    motor.neutral()
    pusher_client.trigger("drive-complete", "Autobot available")

def toggle_green():
    """ Toggle green LED """
    GPIO.output(LED_G, True)
    sleep(0.4)
    GPIO.output(LED_G, False)

def toggle_red():
    """ Toggle red LED """
    GPIO.output(LED_R, True)
    sleep(0.4)
    GPIO.output(LED_R, False)

# Globals
thread = threading.Thread(target=start_drive)
app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Routes
@app.route("/", methods=["GET"])
def home():
    """ Render docs page """
    return "Autobot API"

@app.route("/forward", methods=["GET"])
def forward():
    """ Move bot forward """
    global thread
    if thread.isAlive(): return "Autobot busy"
    thread = threading.Thread(target=start_drive, args=["FORWARD"])
    thread.start()
    return "Moved forward"

@app.route("/reverse", methods=["GET"])
def reverse():
    """ Move bot backward """
    global thread
    if thread.isAlive(): return "Autobot busy"
    thread = threading.Thread(target=start_drive, args=["REVERSE"])
    thread.start()
    return "Moved backward"

@app.route("/left", methods=["GET"])
def turn_left():
    """ Turn bot left """
    global thread
    if thread.isAlive(): return "Autobot busy"
    thread = threading.Thread(target=start_drive, args=["LEFT"])
    thread.start()
    return "Turned left"

@app.route("/right", methods=["GET"])
def turn_right():
    """ Turn bot right """
    global thread
    if thread.isAlive(): return "Autobot busy"
    thread = threading.Thread(target=start_drive, args=["RIGHT"])
    thread.start()
    return "Turned right"

@app.route("/activate", methods=["GET"])
def activate():
    """ Activate autobot """
    global thread
    if thread.isAlive(): return "Autobot busy"
    thread = threading.Thread(target=start_drive, args=["AUTO"])
    thread.start()
    return "Autobot on"

@app.route("/deactivate", methods=["GET"])
def deactivate():
    """ Deactivate auto """
    collision.stop()
    motor.neutral()
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

    # Sound Sensor
    TRIG = 16
    ECHO = 18

    # Trigger distance
    TRIG_D = 40

    motor = Motor(LEFT1, LEFT2, RIGHT1, RIGHT2)
    sensor = soundsensor.Sensor(TRIG_D, TRIG, ECHO, LED_G, LED_R)
    motor.setup_GPIO()
    sensor.setup_GPIO()
    sensor.set_HUD = False

    collision = Collision(sensor, motor)

    try:
        toggle_green()
        toggle_red()
        toggle_green()
        toggle_red()
        toggle_green()
        toggle_red()
        app.run(host='0.0.0.0', port=3000)

        toggle_green()
        sleep(0.5)
        toggle_green()
        pusher_client.trigger("api-status", "Online")
    except KeyboardInterrupt:
        motor.neutral()
        GPIO.cleanup()
