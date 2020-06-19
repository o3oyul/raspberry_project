import os
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import sys
sys.path.append('../')
import time

from DFRobot_MAX17043 import DFRobot_MAX17043
import RPi.GPIO as GPIO

gauge = DFRobot_MAX17043()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

def interruptCallBack(channel):
  gauge.clearInterrupt()
  print('Low power alert interrupt!')
  #put your battery low power alert interrupt service routine here
  
GPIO.add_event_detect(7, GPIO.FALLING, callback = interruptCallBack, bouncetime = 5)

rslt = gauge.begin()

while rslt != 0:
  print('gauge begin faild')
  time.sleep(2)
  rslt = gauge.begin()

gauge.setInterrupt(32) #use this to modify alert threshold as 1% - 32% (integer)
print('gauge begin successful')
  
fig = plt.figure()
ax = plt.axes(xlim=(0,150),ylim=(3500,5500))
line,=ax.plot([],[],lw=1,c='blue',marker='d',ms=2)
max_points=150
line,=ax.plot(np.arange(max_points),np.ones(max_points,dtype=np.float)*np.nan, lw=1, c='blue', marker='d', ms=2)

def init():
    return line

vol = gauge.readVoltage()
def get_y():
    time.sleep(0.2)
    vol=gauge.readVoltage()
    return vol

def animate(i):
    y=get_y()
    old_y=line.get_ydata()
    new_y=np.r_[old_y[1:],y]
    line.set_ydata(new_y)
    print(y)
    return line,
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200,interval=20, blit=False)
plt.show()
'''
while True:
  time.sleep(2)
  print('voltage: ' + str(gauge.readVoltage()) + 'mV')
  print('percentage: ' + str(round(gauge.readPercentage(), 2)) + '%')
'''
