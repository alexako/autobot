# Autobot

A simple autonomous car bot powered by a Raspberry Pi. An ultrasonic sound sensor is used to detect and avoid any obstacles directly in front of the bot. Code has been abstracted to be available for use in other applications.

#### Motor control
The `motor.py` file can be used as a an object like so:
```python
import motor
move = motor.Motor(left_pin1, left_pin2, right_pin1, right_pin2)
move.setup_GPIO() # Set up GPIO board/pins
move.forward()
```
Each direction function, (`forward(), reverse(), left(), right(), neutral()`), runs in infinite loops.

#### Sound sensor
The 'soundsensor.py' program runs and measures a distance only once by default before the program ends. A real-time measurement display is also available.
```python
import soundsensor as sound
s = sound.Sensor(trigger_distance, trigger_pin, echo_pin, led_pin1, led_pin2)
s.setup_GPIO()          # Set up GPIO board/pins
s.HUD = True            # Enables real-time measure print to console (optional, default: True)
s.enable_loop = True    # Enables infinite loop (optional, default: False)
s.start()               # Start measurement
```

#### Collision detection
This relies on both `soundsensor.py` and `motor.py` to function. Super simple AI. It moves forward until an obstacle is detected, then turns left until an obstacle is no longer detected before continuing forward.