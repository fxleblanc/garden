#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import datetime
import schedule
import signal
import sys

relay = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)

def lights_on():
    print("Lights on")
    GPIO.output(relay, False)

def lights_off():
    print("Lights off")
    GPIO.output(relay, True)

def signal_handler(sig, frame):
    GPIO.cleanup()
    print("Exiting")
    sys.exit(0)


start = "8:00"
close = "23:00"

current_hour = datetime.datetime.now().hour
start_hour = int(start.split(":")[0])
close_hour = int(close.split(":")[0])

if current_hour < start_hour or current_hour > close_hour:
    lights_off()
else:
    lights_on()

schedule.every().day.at("8:00").do(lights_on)
schedule.every().day.at("23:00").do(lights_off)

signal.signal(signal.SIGINT, signal_handler)

print("Starting lights service")
while True:
    schedule.run_pending()
    time.sleep(1)
