import random
import soundsensor
import motor
import time
import RPi.GPIO as GPIO


def drive(sensor, move):
    """ Arguments are sensor and motor control objects"""

    def obstacle():
        return sensor.distance < sensor.trigger_distance

    def turn(direction):
        if direction == "LEFT":
            return move.left()
        return move.right()

    while True:
        direction = random.choice(["LEFT", "RIGHT"])
        last_detection = time.time()
        attempts = 0
        sensor.start()
        if not obstacle():
            move.forward()
        else: # Scan for obstacles

            if last_detection:
                if (time.time() - last_detection) < 1:
                    if direction == "LEFT":
                        direction = "RIGHT"
                    else:
                        direction = "LEFT"

            while obstacle():
                sensor.start()
                turn(direction)
                time.sleep(0.1)
                move.neutral()
                time.sleep(0.05)
                attempts += 1
                sensor.start()
                if obstacle() and attempts > 2:
                    move.right()
                    time.sleep(0.2)
                    sensor.start()
                    if obstacle():
                        direction = "RIGHT"
                        attempts = 0


if __name__ == '__main__':

    # ## Pin setup
    # Motor
    left1 = 31
    left2 = 33
    right1 = 35
    right2 = 37

    # Sound sensor
    trig = 16
    echo = 18
    led_r = 7
    led_g = 11
    trig_d = 40 # Trigger distance

    try:
        m = motor.Motor(left1, left2, right1, right2)
        s = soundsensor.Sensor(trig_d, trig, echo, led_g, led_r)
        m.setup_GPIO()
        s.setup_GPIO()
        s.set_HUD = False
        drive(s, m)

    except KeyboardInterrupt:
        m.neutral()
        GPIO.cleanup()
