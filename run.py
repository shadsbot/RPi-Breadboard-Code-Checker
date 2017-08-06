import RPi.GPIO as GPIO
import time
import sys
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 4  17  22
pinNum = [0,0,0]
pinNum[0] = int(sys.argv[1])
pinNum[1] = int(sys.argv[2])
pinNum[2] = int(sys.argv[3])

# 18 23 24 25
errPin = [0,0,0,0]
errPin[0] = int(sys.argv[4])
errPin[1] = int(sys.argv[5])
errPin[2] = int(sys.argv[6])
errPin[3] = int(sys.argv[7])

ERR = pinNum[2]
WARN= pinNum[1]
GOOD= pinNum[0]

linenum = []

file = sys.argv[8]
sleepTime = 1

# 18 input
GPIO.setup(27, GPIO.IN)

#Batman: Turn off the Dark
for pin in pinNum:
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin,GPIO.LOW)
for pin in errPin:
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin,GPIO.LOW)

GPIO.output(WARN,GPIO.HIGH)
proc = subprocess.check_output(['./compile.sh',file])
GPIO.output(WARN,GPIO.LOW)

if proc == "\n":
	GPIO.output(GOOD,GPIO.HIGH)
else:
	GPIO.output(ERR,GPIO.HIGH)
	proc = proc.strip()
	linenum = list(proc)
	while True:
		for line in linenum:
			if line == "1":
				GPIO.output(errPin[3],GPIO.HIGH)
			elif line == "2":
				GPIO.output(errPin[2],GPIO.HIGH)
			elif line == "3":
				GPIO.output(errPin[2],GPIO.HIGH)
				GPIO.output(errPin[3],GPIO.HIGH)
			elif line == "4":
				GPIO.output(errPin[1],GPIO.HIGH)
			elif line == "5":
				GPIO.output(errPin[1],GPIO.HIGH)
				GPIO.output(errPin[3],GPIO.HIGH)
			elif line == "6":
				GPIO.output(errPin[2],GPIO.HIGH)
				GPIO.output(errPin[1],GPIO.HIGH)
			elif line == "7":
				GPIO.output(errPin[3],GPIO.HIGH)
				GPIO.output(errPin[2],GPIO.HIGH)
				GPIO.output(errPin[1],GPIO.HIGH)
			elif line == "8":
				GPIO.output(errPin[0],GPIO.HIGH)
			elif line == "9":
				GPIO.output(errPin[0],GPIO.HIGH)
				GPIO.output(errPin[3],GPIO.HIGH)

			# Keep it on for a bit, then shut it off
			time.sleep(sleepTime)
			for pin in errPin:
				GPIO.output(pin,GPIO.LOW)
		# Flash to indicate we need to restart
		for i in range(0,3):
			for pin in errPin:
				GPIO.output(pin,GPIO.HIGH)
			time.sleep(0.2)
			for pin in errPin:
				GPIO.output(pin,GPIO.LOW)
			time.sleep(0.2)
