import RPi.GPIO as GPIO
import pygame


def PS2Controller():

    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    print 'Initialized Joystick : %s' % j.get_name()

    RightTrack = 0
    LeftTrack = 0

    threshold = 0.60

    while True:
        UpdateMotors = 0
        events = pygame.event.get()
        for event in events:
            if event.type == 7:
                if event.value > -1.0 or event.value < -1.5:
                    if event.axis == 1:
                        LeftTrack = event.value
                        UpdateMotors = 1
                    elif event.axis == 3:
                        RightTrack = event.value
                        UpdateMotors = 1

        # Check if we need to update what the motors are doing
        if UpdateMotors:
            GPIO.output(led_r, 0)
            GPIO.output(led_g, 1)

            # Check how to configure the left motor

            # Move forwards
            if (RightTrack < -threshold):
                GPIO.output(right1, 1)
                GPIO.output(right2, 1)
            # Move backwards
            elif (RightTrack > threshold):
                GPIO.output(right1, 1)
                GPIO.output(right2, 0)
            # Stopping
            else:
                GPIO.output(right1, 0)
                GPIO.output(right2, 1)
                GPIO.output(led_g, 0)
                GPIO.output(led_r, 1)

            # And do the same for the right motor
            if (LeftTrack < -threshold):
                GPIO.output(left1, 1)
                GPIO.output(left2, 0)
            # Move backwards
            elif (LeftTrack > threshold):
                GPIO.output(left1, 1)
                GPIO.output(left2, 1)
            # Otherwise stop
            else:
                GPIO.output(left1, 0)
                GPIO.output(left2, 0)
                GPIO.output(led_g, 0)
                GPIO.output(led_r, 1)



if __name__ == '__main__':

    #Motor Pins
    left1 = 31
    left2 = 33
    right1 = 35
    right2 = 37

    #LEDs
    led_r = 7
    led_g = 11

    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(left1, GPIO.OUT)
        GPIO.setup(left2, GPIO.OUT)
        GPIO.setup(right1, GPIO.OUT)
        GPIO.setup(right2, GPIO.OUT)
        GPIO.setup(led_r, GPIO.OUT)
        GPIO.setup(led_g, GPIO.OUT)

        PS2Controller()
    except KeyboardInterrupt:
        GPIO.cleanup()
