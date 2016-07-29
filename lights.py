#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import datetime
import schedule
import signal
import sys

relay = 23
fan = 18

start = "8:00"
close = "23:00"

start_hour = int(start.split(":")[0])
close_hour = int(close.split(":")[0])

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(fan, GPIO.OUT)



def lights_on():
    print("Lights on")
    GPIO.output(relay, True)


def lights_off():
    print("Lights off")
    GPIO.output(relay, True)


def fan_on():
    now = datetime.datetime.now()
    if now.hour > start_hour and now.hour < close_hour:
        GPIO.output(fan, False)
        time.sleep(300000)
        fan_off()


def fan_off():
    GPIO.output(fan, True)


def signal_handler(sig, frame):
    GPIO.cleanup()
    print("Exiting")
    sys.exit(0)


current_hour = datetime.datetime.now().hour


if current_hour < start_hour or current_hour > close_hour:
    lights_off()
    fan_off()
else:
    lights_on()

schedule.every().day.at("8:00").do(lights_on)
schedule.every().day.at("23:00").do(lights_off)
schedule.every().hour.do(fan_on)

signal.signal(signal.SIGINT, signal_handler)

print("Starting lights service")
while True:
    schedule.run_pending()
    time.sleep(1)
