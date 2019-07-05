import random
import soundsensor
import motor
import time
import RPi.GPIO as GPIO


class Collision():
    """ Arguments are sensor and motor control objects"""

    def __init__(self, sensor, move):
        self.activate = True
        self.sensor = sensor
        self.move = move

    def obstacle(self):
        return self.sensor.distance < self.sensor.trigger_distance

    def turn(self, direction):
        if direction == "LEFT":
            return self.move.left()
        return self.move.right()

    def drive(self):
        while self.activate:
            direction = random.choice(["LEFT", "RIGHT"])
            last_detection = time.time()
            attempts = 0
            self.sensor.start()
            if not self.obstacle():
                self.move.forward()
            else: # Scan for obstacles

                if last_detection:
                    if (time.time() - last_detection) < 1:
                        if direction == "LEFT":
                            direction = "RIGHT"
                        else:
                            direction = "LEFT"

                while self.obstacle():
                    self.sensor.start()
                    self.turn(direction)
                    time.sleep(0.1)
                    self.move.neutral()
                    time.sleep(0.05)
                    attempts += 1
                    self.sensor.start()
                    if self.obstacle() and attempts > 2:
                        self.move.right()
                        time.sleep(0.2)
                        self.sensor.start()
                        if self.obstacle():
                            direction = "RIGHT"
                            attempts = 0

    def start(self):
        self.activate = True

    def stop(self):
        self.activate = False


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

        c = Collision(s, m)
        c.start()
        c.drive()

    except KeyboardInterrupt:
        m.neutral()
        GPIO.cleanup()
