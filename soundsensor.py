import RPi.GPIO as GPIO
import time
import sys


class Sensor(object):
    """ Arguments [trigger_distance, trig_pin, echo_pin, led_g, led_r] """

    def __init__(self, trigger_distance, trig_pin, echo_pin, led_g, led_r):
        self.trigger_distance = trigger_distance
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.led_g = led_g
        self.led_r = led_r
        self.distance = 0 
        self.HUD = True
        self.enable_loop = False

    def setup_GPIO(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.setup(self.led_g, GPIO.OUT)
        GPIO.setup(self.led_r, GPIO.OUT)

    def start(self):
        try:
            while 1: 
                GPIO.output(self.trig_pin, False)
                time.sleep(0.1)

                #Send sound signal
                GPIO.output(self.trig_pin, True)
                time.sleep(0.00001)
                GPIO.output(self.trig_pin, False)

                #Time signal's return
                while GPIO.input(self.echo_pin) == 0:
                    pulse_start = time.time()

                while GPIO.input(self.echo_pin) == 1:
                    pulse_end = time.time()

                pulse_duration = pulse_end - pulse_start
                self.distance = pulse_duration * 17150
                self.distance = round(self.distance, 2)

                #Distance output
                if self.HUD:
                    sys.stdout.write('\r')
                    sys.stdout.write("Distance in cm: %r " % self.distance)
                    sys.stdout.flush()

                #LEDs
                if self.distance > self.trigger_distance:
                    GPIO.output(self.led_r, False)
                    GPIO.output(self.led_g, True)
                else: 
                    GPIO.output(self.led_g, False)
                    GPIO.output(self.led_r, True)
                    time.sleep(0.05)

                if not self.enable_loop: break

        except KeyboardInterrupt:
            GPIO.cleanup()
            print ""


if __name__ == '__main__':

    #Pin Setup
    TRIG = 16
    ECHO = 18
    LED_G = 11
    LED_R = 7

    # Distance for trigger in cm
    trig_d = 50

    sensor = Sensor(trig_d, TRIG, ECHO, LED_G, LED_R)
    sensor.setup_GPIO()
    sensor.enable_loop = True
    print "Distance measurement in progress..."
    sensor.start()
