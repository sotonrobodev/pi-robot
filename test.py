# usage:
#   mkfifo startfifo
#   python2 test.py --startfifo startfifo &                 # start the script in the background. waits for start button info to be sent.
#   echo '{"zone":0,"mode":"dev","arena":"A"}' > startfifo  # send start info.


import time
from sr.robot import *

#power = 0
#dir = 1
#while True:
#  power += dir
#  R.motors[0].m0.power = power
#  if abs(power) == 100:
#    dir = -dir
#  time.sleep(0.02)

#while True:
#  R.ruggeduinos[0].digital_write(13, True)
#  time.sleep(1)
#  R.ruggeduinos[0].digital_write(13, False)
#  time.sleep(1)

def constrain(x, low, high):
  if x < low:
    x = low
  if x > high:
    x = high
  return x

def map(x, a, b, c, d):
  return (float(x - a) / float(b - a)) * (d - c) + c

SERVO_TICKS_MIN = 150
SERVO_TICKS_MAX = 600

class CustomRuggeduino(Ruggeduino):
    def set_servo(self, channel, pos):
        pos = int(map(pos, -100.0, 100.0, SERVO_TICKS_MIN, SERVO_TICKS_MAX))
        pos = constrain(pos, SERVO_TICKS_MIN, SERVO_TICKS_MAX)
        channel_char = chr(ord("a") + channel)
        pos_high_char = chr(pos >> 8)
        pos_low_char = chr(pos & 255)
        cmd = "s" + channel_char + pos_high_char + pos_low_char
        with self.lock:
            self.command(cmd)

R = Robot.setup()
R.ruggeduino_set_handler_by_fwver("Beeduino", CustomRuggeduino)
R.init()
R.wait_start()

while True:
  R.ruggeduinos[0].set_servo(1, -100)
  time.sleep(1)
  R.ruggeduinos[0].set_servo(1, 100)
  time.sleep(1)


