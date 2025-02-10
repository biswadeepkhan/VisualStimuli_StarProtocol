from psychopy import visual, core, event ,monitors
from win32api import GetSystemMetrics
import numpy as np
import time
from itertools import permutations, repeat
from datetime import datetime
import random
import u3

#create a window
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
print(width)
print(height)
monitor_size = [1280,800]

myMonitor = monitors.Monitor('X1_carbon',width =31)
myMonitor.setSizePix(monitor_size)
myMonitor.saveMon()

refresh_rate = 59 # refresh rate of your current monitor settings in Hz

'=======================DOT PARAMETERS============================'
distance = 0.15 #cm, distance between the screen and larvae's head
direction = 'r'       # starting direction of the dot with respect to fish
x_distance = 160# degrees, full range. Moving distance from left to right in terms of visual angle, which takes 1/2 of total time
speed=200


x_distance=160
if direction == 'r':
    x_distance = np.abs(x_distance)
elif direction == 'l':
    x_distance = -np.abs(x_distance)

moving_time = x_distance/float(speed) # second
position = [-x_distance/2.0, 0]

dt = 10
dev = u3.U3()  # Open first found U3

dev.getCalibrationData()
dev.configIO(EnableCounter1=True,TimerCounterPinOffset=7)

myWin = visual.Window(monitor_size, monitor=myMonitor, units='degFlat', color = (-1,-1,-1), fullscr=True,viewPos=[0,0])

'''Get the the average time per frame'''
frametime = myWin.getMsPerFrame(nFrames=60, showVisual=False, msg='', msDelay=0.0)[0]

# return the the average time per frame, with unit of ms
deg_per_frame = frametime*speed/1000
y_deg_per_frame = frametime*200/1000
count=0
timer = core.Clock()
prev_count=0


while True:
    count = int(np.array(dev.getFeedback(u3.Counter(counter=1))))
    print(count)
    if count != prev_count:
        prev_count = count
        timer = core.Clock()
        time.sleep(3)
        t0 = timer.getTime()
        if direction == 'r' or 'l':
         timer.reset()
         myStim = visual.Circle(win=myWin, lineWidth=0, radius=4/2, units='degFlat',fillColor=[1, 1, 1], pos=position,contrast=1)
         #position = [-x_distance / 2.0, 0]
         while position[0] <= x_distance/2.0:
            position[0] += deg_per_frame
            myStim.setPos(position)
            myStim.draw()
            myWin.update()

        while position[0] >= -x_distance/2.0:
            position[0] -= deg_per_frame
            myStim.setPos(position)
            myStim.draw()
            myWin.update()

        timeUse = timer.getTime()
        print(timeUse)
        myWin.flip(clearBuffer=True)
        myWin.update()
        timeUse = timer.getTime()
        time.sleep(10 - (3+timeUse))
        timeUse1 = timer.getTime()
        print(timeUse1 - timeUse)

    prev_count = count
    if "escape" in event.getKeys():
        core.quit()


#cleanup
core.quit()
