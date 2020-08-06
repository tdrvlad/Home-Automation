import RPi.GPIO as GPIO
import time
#----------------------------------

irigation_time = 15 #(minute)

#----------------------------------

# GPIO MAP
# GPIO 2 - Relay 4 - Power 5v for Remote Relays
# GPIO 4 - Relay 2 - Irigation Pump Remote Relay (Ground to INPUT of Remote Relay)

relay_power = 2
relay_pump = 4

#Setting up GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(relay_power,GPIO.OUT)
GPIO.output(relay_power,GPIO.LOW)

GPIO.setup(relay_pump,GPIO.OUT)
GPIO.output(relay_pump,GPIO.LOW)

time.sleep(60 * irigation_time)

GPIO.output(relay_pump,GPIO.HIGH)
GPIO.output(relay_power,GPIO.HIGH)

GPIO.cleanup()



