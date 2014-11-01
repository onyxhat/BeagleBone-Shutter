#!/usr/bin/python

###Imports
import cv2
import Adafruit_BBIO.GPIO as GPIO
import time, datetime
import subprocess
import pysftp

###Functions
def get_time():
	return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

def take_picture(file):
	cam = cv2.VideoCapture(0)
	cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1920)
	cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,1080)
	retval, im = cam.read()
	cv2.imwrite(file, im)
	subprocess.call('clear')
	del(cam)

def display_image(file):
    try:
        command = "fbi -a -T 1 %s" % file
        subprocess.call('killall fbi', shell=True)
        viewImg = subprocess.Popen(command, shell=True)
    except:
        print "Unable to display %s" % file

###I/O
GPIO.setup("P8_12", GPIO.IN)
GPIO.setup("P8_10", GPIO.OUT)

###Runtime
#subprocess.call('ntpdate -b -s -u pool.ntp.org')
subprocess.call('clear')
old_switch_state = 0

GPIO.output("P8_10", GPIO.LOW)

while True:
	new_switch_state = GPIO.input("P8_12")
	if new_switch_state == 1 and old_switch_state == 0:
		file = "/pictures/%s.png" % get_time()

		for i in xrange(3, 0, -1):
			print "%i..." % (i)
			time.sleep(1.0)

		GPIO.output("P8_10", GPIO.HIGH)
		print "CHEESE!"
		take_picture(file)
		display_image(file)
		GPIO.output("P8_10", GPIO.LOW)

	old_switch_state = new_switch_state
