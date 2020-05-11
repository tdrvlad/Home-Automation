import RPi.GPIO as GPIO
import time
#----------------------------------

lights_time = 5 #(minute)

#----------------------------------

# GPIO MAP
# GPIO 2 - Relay 4 - Power 5v for Remote Relays
# GPIO 3 - Relay 3 - Lights Remote Relay (Ground to INPUT of Remote Relay)

relay_power = 2
relay_lights = 3

#Setting up GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(relay_power,GPIO.OUT)
GPIO.output(relay_power,GPIO.LOW)

GPIO.setup(relay_lights,GPIO.OUT)
GPIO.output(relay_lights,GPIO.LOW)

time.sleep(60 * lights_time)

GPIO.output(relay_lights,GPIO.HIGH)
GPIO.output(relay_power,GPIO.HIGH)

GPIO.cleanup()



