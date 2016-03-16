import os
import glob
import time
import RPi.GPIO as gpio

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

gpio.setmode(gpio.BOARD)
#set pins to go out
R = 37
G = 35
B = 33
lights = [R,G,B]

for pin in lights:
    gpio.setup(pin, gpio.OUT)

r = gpio.PWM(R,100)
r.start(0)
g = gpio.PWM(G,100)
g.start(0)
b = gpio.PWM(B,100)
b.start(0)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c
	
while True:
	t = read_temp()
	print(t)
	if t > 25:
	    g.ChangeDutyCycle(100)
	else:
	    g.ChangeDutyCycle(0)
	    r.ChangeDutyCycle(100)	
	time.sleep(1)

