import RPi.GPIO as GPIO
import pygame
import os

class BTController():

    def __init__(self):
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        pygame.init()
        pygame.display.init()
        pygame.joystick.init()

        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        print "Initialized:", joystick.get_name()

    def setup_GPIO(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LEFT1, GPIO.OUT)
        GPIO.setup(LEFT2, GPIO.OUT)
        GPIO.setup(RIGHT1, GPIO.OUT)
        GPIO.setup(RIGHT2, GPIO.OUT)
        GPIO.setup(LED_G, GPIO.OUT)
        GPIO.setup(LED_R, GPIO.OUT)

    def start(self):

        accelerate = False
        left_track = 0
        right_track = 0
        threshold = 0.40

        while True:
            update_motors = False
            events = pygame.event.get()

            for event in events:

                # Button pressed
                if event.type == 10:
                    if event.button == 0:
                        accelerate = True
                    elif event.button == 1:
                        accelerate = True

                # Button released
                if event.type == 11:
                    accelerate = False

                # Joysticks
                if event.type == 7:
                    if event.axis == 1:
                        right_track = event.value
                    elif event.axis == 3:
                        left_track = event.value

            if left_track or right_track:
                print event
                GPIO.output(LED_R, 0)
                GPIO.output(LED_G, 1)

                # Right motor - Forward
                if (right_track < -threshold):
                    GPIO.output(RIGHT1, 1)
                    GPIO.output(RIGHT2, 1)
                # Right motor - Backward
                elif (right_track > threshold):
                    GPIO.output(RIGHT1, 1)
                    GPIO.output(RIGHT2, 0)

                # Left motor - Forward
                if (left_track < -threshold):
                    GPIO.output(LEFT1, 1)
                    GPIO.output(LEFT2, 0)
                # Left motor - Backward
                elif (left_track > threshold):
                    GPIO.output(LEFT1, 1)
                    GPIO.output(LEFT2, 1)

            elif (accelerate):
                GPIO.output(LEFT1, 1)
                GPIO.output(LEFT2, 0)
                GPIO.output(RIGHT1, 1)
                GPIO.output(RIGHT2, 1)
                GPIO.output(LED_G, 1)
                GPIO.output(LED_R, 0)

            else:
                GPIO.output(LEFT1, 0)
                GPIO.output(LEFT2, 1)
                GPIO.output(RIGHT1, 0)
                GPIO.output(RIGHT2, 0)
                GPIO.output(LED_G, 0)
                GPIO.output(LED_R, 1)



if __name__ == '__main__':

    LED_G = 11
    LED_R = 7

    # Motors
    LEFT1 = 31
    LEFT2 = 33
    RIGHT1 = 35
    RIGHT2 = 37

    try:
        bt = BTController()
        bt.setup_GPIO()
        bt.start()
    except KeyboardInterrupt:
        GPIO.cleanup()
