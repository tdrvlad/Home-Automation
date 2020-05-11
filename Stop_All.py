import RPi.GPIO as GPIO
import time
#----------------------------------

lights_time = 45 #(minute)

#----------------------------------

# GPIO MAP
# GPIO 2 - Relay 4 - Power 5v for Remote Relays
# GPIO 3 - Relay 3 - Lights Remote Relay (Ground to INPUT of Remote Relay)
# GPIO 4 - Relay 2 - Irigation Pump Remote Relay (Ground to INPUT of Remote Relay)
# GPIO 17 - Relay 1 - Christimas Lights Remote Relay (Ground to INPUT of Remote Relay)

relay_power = 2
relay_lights = 3
relay_pump = 4
relay_christmas_lights = 17

#Setting up GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(relay_power,GPIO.OUT)
GPIO.output(relay_power,GPIO.HIGH)

GPIO.setup(relay_lights,GPIO.OUT)
GPIO.output(relay_lights,GPIO.HIGH)

GPIO.setup(relay_pump,GPIO.OUT)
GPIO.output(relay_pump,GPIO.HIGH)

GPIO.setup(relay_christmas_lights,GPIO.OUT)
GPIO.output(relay_christmas_lights,GPIO.HIGH)

GPIO.cleanup()



