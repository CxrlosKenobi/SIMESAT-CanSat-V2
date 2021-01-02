from matplotlib.animation import FuncAnimation
from colorama import init, Fore, Back, Style
import matplotlib.animation as animation
from numpy.random import seed, rand
import matplotlib.pyplot as plt
from random import random, seed
import os, string, random
import datetime as dt
import pandas as pd
import numpy as np
from time import *
os.system('clear')


#Plotting data into Command Line Interface with lists
'''
xValue = random.random()
yValue = random.random()
zValue = random.random()

xValue = round(xValue, 4)
yValue = round(yValue, 4)
zValue = round(zValue, 4)

lst = [xValue, yValue, zValue]

c = random.uniform(15, 28)
temp = round(c, 2)


print('\t#.....MPU9250 in 0x68 Address at ' + Style.RESET_ALL + '.....#\n')
print(Back.WHITE + Fore.BLACK + 'Accelerometer: ' + str(lst) + Style.RESET_ALL)
print(Back.WHITE + Fore.BLACK + 'Gyroscope:     ' + str(lst) + Style.RESET_ALL)
print(Back.WHITE + Fore.BLACK + 'Magnetometer:  ' + str(lst) + Style.RESET_ALL)
print(Back.WHITE + Fore.BLACK + 'Temperature:   ' + str(temp) + Style.RESET_ALL)
print('\n')



while True:
    test(hr, min, sec)
    sleep(1)
'''


# Plotting the 3D Gyroscope data
'''
plt.style.use('ggplot')
sleep(1)

xValue = round(random.random(), 6)
yValue = round(random.random(), 6)
zValue = round(random.random(), 6)

ii = 100
t1 = time()

# prepping for visualization
mpu6050_str = ['accel-x', 'accel-y', 'accel-z', 'gyro-x', 'gyro-y', 'gyro-z']
AK8963_str = ['mag-x','mag-y','mag-z']

mpu6050_vec, AK8963_vec, t_vec = [], [], []

print('recording data')
for ii in range(0, ii):
    mx,my,mz, ax,ay,az, wx,wy,wz = random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random()

    t_vec.append(time()) # capture timestamp
    AK8963_vec.append([mx, my, mz])
    mpu6050_vec.append([ax, ay, az, wx, wy, wz])

print('sample rate accel: {} Hz'.format(ii/(time()-t1))) # print the sample rate
t_vec = np.subtract(t_vec, t_vec[0])

# plot the resulting data in 3-subplots, with each data axis
fig, axs = plt.subplots(3, 1, figsize=(12,7), sharex=True)
cmap = plt.cm.Set1

ax = axs[0] # plot Accelerometer data
for zz in range(0, np.shape(mpu6050_vec)[1]-3):
    data_vec = [ii[zz] for ii in mpu6050_vec]
    ax.plot(t_vec,data_vec, label=mpu6050_str[zz], color=cmap(zz))
ax.legend(bbox_to_anchor=(1.12, 0.9))
ax.set_ylabel('Acceleration [g]', fontsize=12)

ax2 = axs[1] # plot Gyroscope data
for zz in range(3,np.shape(mpu6050_vec)[1]):
    data_vec = [ii[zz] for ii in mpu6050_vec]
    ax2.plot(t_vec, data_vec, label=mpu6050_str[zz], color=cmap(zz))
ax2.legend(bbox_to_anchor=(1.12, 0.9))
ax2.set_ylabel('Angular Vel. [dps]', fontsize=12)

ax3 = axs[2] # plot Magnetometer data
for zz in range(0, np.shape(AK8963_vec)[1]):
    data_vec = [ii[zz] for ii in AK8963_vec]
    ax3.plot(t_vec, data_vec, label=AK8963_str[zz], color=cmap(zz+6))
ax3.legend(bbox_to_anchor=(1.12, 0.9))
ax3.set_ylabel('Magn. Field [Î¼T]', fontsize=12)
ax3.set_xlabel('Time [s]', fontsize=14)

fig.align_ylabels(axs)
plt.show()
'''


# Real time plot with matplotlib
'''
plt.style.use('seaborn')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

def animation(i):
    AAPL_STOCK = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv')
    x = []
    y = []

    x = AAPL_STOCK[0:i]['AAPL_x']
    y = AAPL_STOCK[0:i]['AAPL_y']

    ax.clear()
    ax.plot(x, y)

animation = FuncAnimation(fig, func=animation, interval=1)
plt.show()
'''



# Real time plot with matplotlib option2
plt.style.use('seaborn')

def live_plotter(x_vec, y1_data, line1, title='', y_label='', pause_time=0.1):
    if line1 == []:
        #This is the call to matplotlib that allows dynamic plotting
        plt.ion()

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(111)

        # Create a variable for the line so we can later update it
        line1, = ax.plot(x_vec, y1_data, color='red', alpha=0.5)

        #Update plot label/title
        plt.ylabel(f'{y_label}')
        plt.title(f'{title}')

        plt.show()

    # After the figure, axis, and line are created...
    # We only need update the y-data
    line1.set_ydata(y1_data)

    # Adjust limits if new data goes beyond bounds
    if np.min(y1_data) <= line1.axes.get_ylim()[0] or np.max(y1_data) >= line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data) - np.std(y1_data), np.max(y1_data) + np.std(y1_data)])

    # This pauses the data so the figure/axis can catch up
    # The amount of pause can be altered above
    plt.pause(pause_time)

    # Return line so we can update it again in the next iteration
    return line1
# The user can also customize the function to allow dynamic changes of title, x-label, y-label, x-limits, etc.
# line1.set_ydata(y1_data) can also be switched to line1.set_data(x_vec,y1_data) to change both x and y data on the plots.

size = 100
x_vec = np.linspace(0, 1, size+1)[0:-1]
y_vec = np.random.randn(len(x_vec))
line1 = []


while True:
    try:
        rand_val = np.random.randn(1)
        y_vec[-1] = rand_val
        line1 = live_plotter(x_vec, y_vec, line1, title='Plotting with random data for now', y_label='Y-Label')
        y_vec = np.append(y_vec[1:], 0.0)
    except KeyboardInterrupt:
        print('\nStopped')
        exit()
