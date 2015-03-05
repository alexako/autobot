import soundsensor
import motor
import time
import RPi.GPIO as GPIO


def drive(sensor, move):
    """ Argument is sensor and motor control objects"""

    def obstacle():
        return sensor.distance < sensor.trigger_distance

    while True:
        sensor.start()
        start = time.time()
        if not obstacle():
            move.forward()
        else: #Scan for obstacles
            while obstacle():
                sensor.start()
                move.left()
            move.left()
            time.sleep(0.1)


if __name__ == '__main__':

    ### Pin setup
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

#    except KeyboardInterrupt:
    except KeyboardInterrupt:
        m.neutral()
        GPIO.cleanup()
