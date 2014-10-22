#!/usr/bin/python

###Imports
import cv2
import Adafruit_BBIO.GPIO as GPIO
import time, datetime
import os
import pysftp
import futures

###Functions
def get_time():
	return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

def take_picture(file):
	cam = cv2.VideoCapture(0)
	cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1920)
	cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,1080)
	retval, im = cam.read()
	cv2.imwrite(file, im)
	os.system('clear')
	del(cam)

def upload_sftp(file, server, username, password):
	try:
		with pysftp.Connection(server, username=username, password=password) as sftp:
			with sftp.cd('gallery.nuptiae.us/pictures'):
				sftp.put(file)
	except:
		print "Unable to upload file."

###I/O
GPIO.setup("P8_12", GPIO.IN)
GPIO.setup("P8_10", GPIO.OUT)

###Runtime
#os.system('ntpdate -b -s -u pool.ntp.org')
os.system('clear')
old_switch_state = 0
executor = futures.ProcessPoolExecutor(max_workers=1)

GPIO.output("P8_10", GPIO.LOW)

while True:
	new_switch_state = GPIO.input("P8_12")
	if new_switch_state == 1 and old_switch_state == 0:
		file = "/pictures/" + get_time() + ".png"

		for i in xrange(3, 0, -1):
			print "%i..." % (i)
			time.sleep(1.0)

		print "CHEESE!"

		GPIO.output("P8_10", GPIO.HIGH)
		take_picture(file)
		#future = executor.submit(upload_sftp, file, 'ftp.sername.com', 'username', 'password')
		GPIO.output("P8_10", GPIO.LOW)

	old_switch_state = new_switch_state
