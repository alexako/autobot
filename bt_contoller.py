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
        GPIO.setup(LED_G, GPIO.OUT)
        GPIO.setup(LED_R, GPIO.OUT)

    def start(self):
        try:
            while True:
                events = pygame.event.get()

                for event in events:
                    print event

                    if event.type == 10:
                        if event.button == 0:
                            GPIO.output(LED_G, True)
                        elif event.button == 1:
                            GPIO.output(LED_R, True)

                    if event.type == 11:
                        if event.button == 0:
                            GPIO.output(LED_G, False)
                        elif event.button == 1:
                            GPIO.output(LED_R, False)

        except KeyboardInterrupt:
            GPIO.cleanup()
            print ""


if __name__ == '__main__':

    LED_G = 11
    LED_R = 7

    bt = BTController()
    bt.setup_GPIO()
    bt.start()

