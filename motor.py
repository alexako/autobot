import RPi.GPIO as GPIO


class Motor(object):
    """ Args pins [left1, left2, right1, right2] """

    def __init__(self, left1, left2, right1, right2):
        self.left1 = left1
        self.left2 = left2
        self.right1 = right1
        self.right2 = right2

    def setup_GPIO(self):
        GPIO.setmode(GPIO.BOARD)
        #Left motor
        GPIO.setup(self.left1, GPIO.OUT)
        GPIO.setup(self.left2, GPIO.OUT)
        #Right motor
        GPIO.setup(self.right1, GPIO.OUT)
        GPIO.setup(self.right2, GPIO.OUT)

    def reverse(self):
        GPIO.output(self.left1, 1)
        GPIO.output(self.left2, 1)
        GPIO.output(self.right1, 1)
        GPIO.output(self.right2, 0)

    def neutral(self):
        GPIO.output(self.left1, 0)
        GPIO.output(self.left2, 0)
        GPIO.output(self.right1, 0)
        GPIO.output(self.right2, 1)

    def forward(self):
        GPIO.output(self.left1, 1)
        GPIO.output(self.left2, 0)
        GPIO.output(self.right1, 1)
        GPIO.output(self.right2, 1)

    def left(self):
        GPIO.output(self.left1, 1)
        GPIO.output(self.left2, 0)
        GPIO.output(self.right1, 1)
        GPIO.output(self.right2, 0)

    def right(self):
        GPIO.output(self.left1, 1)
        GPIO.output(self.left2, 1)
        GPIO.output(self.right1, 1)
        GPIO.output(self.right2, 1)


if __name__ == '__main__':

    LEFT1 = 31
    LEFT2 = 33
    RIGHT1 = 35
    RIGHT2 = 37

    motor = Motor(LEFT1, LEFT2, RIGHT1, RIGHT2)
    motor.setup_GPIO()
    try:
        motor.neutral()
        while True:
            choice = raw_input("w:Forward\na:Left\nd:Right\ne:Neutral\n> ")
            if choice == 'w':
                motor.forward()
            elif choice == 'a':
                motor.left()
            elif choice == 'd':
                motor.right()
            elif choice == 's':
                motor.reverse()
            elif choice == 'e':
                motor.neutral()
            else:
                GPIO.cleanup()
                break

    except KeyboardInterrupt:
        GPIO.cleanup()
