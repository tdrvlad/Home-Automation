import RPi.GPIO as GPIO
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import fbchat
import sys

#------------ Bot Credentials ------------ 

email = "tdrvlad@gmail.com"
password = "12345678901234567890"

command_password = "****"

#------------ Commands Times ------------ 

lights_sum_h = 21   #Summer lights starting hour
lights_sum_m = 30	#Summer lights starting minutes

lights_win_h = 20	#Winter lights starting hour
lights_win_m = 30	#Winter lights starting minutes

lights_dur_h = 0	#Lights duration hour
lights_dur_m = 45	#Lights duration minutes

lights_hourly_dur_m = 5	#Hourly lights duration minutes

irigation_h = 8		#Irigation starting hour
irigation_m = 30	#Irigation starting minutes

irigation_dur_m = 20	#Irigation duration minutes


#------------ GPIO mapping ------------ 

# GPIO 2 - Relay 4 - Power 5v for Remote Relays
# GPIO 3 - Relay 3 - Lights Remote Relay (Ground to INPUT of Remote Relay)
# GPIO 4 - Relay 2 - Irigation Pump Remote Relay (Ground to INPUT of Remote Relay)
# GPIO 17 - Relay 1 - Christimas Lights Remote Relay (Ground to INPUT of Remote Relay)

relay_power = 2
relay_lights = 3
relay_pump = 4
relay_christmas_lights = 17

#------------ Other parameters ------------ 

log_file = 'log.txt'

default_run_time = 20 #minutes

#Commands and Devices dictionaries
commands = {'turn on' : 1, 'turn off' : 0, 'report' : 2}
alt_commands = {'💡' : 1, 'start' : 1, 'stop' : 0, 'delete command' : 0, 'clear command' : 0, 'summary' : 2}

devices = {'Lights' : 1}
alt_devices = {'illumination' : 1, '💡' : 1}

commands.update(alt_commands)
devices.update(alt_devices)

hello_message = 'Hello!'
passwd_req = 'Please, type the password'

#------------ Command functions ------------ 

def log_event(string):
	
	current_time =  datetime.now().strftime('%H:%M:%S')

	f = open(log_file,'a')
	f.write(string + ' at ' + current_time)
	f.close()

def setup_gpio():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	GPIO.setup(relay_power,GPIO.OUT)
	GPIO.setup(relay_lights,GPIO.OUT)
	GPIO.setup(relay_pump,GPIO.OUT)
	GPIO.setup(relay_christmas_lights,GPIO.OUT)

	stop_all()

	log_event('Initialized')

def stop_all(thread):
	GPIO.output(relay_lights,GPIO.HIGH)
	GPIO.output(relay_power,GPIO.HIGH)
	GPIO.output(relay_pump,GPIO.HIGH)
	GPIO.output(relay_christmas_lights,GPIO.HIGH)

def lights_on(thread):
	GPIO.output(relay_power,GPIO.LOW)
	GPIO.output(relay_lights,GPIO.LOW)
	
	log_event('Lights turned on')

	if thread != None:
		thread.send_text('Lights turned on')

def lights_off(thread):
	GPIO.output(relay_power,GPIO.HIGH)
	GPIO.output(relay_lights,GPIO.HIGH)
	
	log_event('Lights turned off')

	if thread != None:
		thread.send_text('Lights turned on')

def christmas_lights_on(thread)
	GPIO.output(relay_christmas_lights,GPIO.LOW)
	GPIO.output(relay_power,GPIO.LOW)

	log_event('Christmas lights turned on')

	if thread != None:
		thread.send_text('Christmas lights turned on')

def christmas_lights_off(thread)
	GPIO.output(relay_christmas_lights,GPIO.HIGH)
	GPIO.output(relay_power,GPIO.HIGH)

	log_event('Christmas lights turned off')

	if thread != None:
		thread.send_text('Christmas lights turned off')

def irigation_on(thread)
	GPIO.output(relay_pump,GPIO.LOW)
	GPIO.output(relay_power,GPIO.LOW)

	log_event('Irigation turned on')

	if thread != None:
		thread.send_text('Irigation turned on')

def irigation_off(thread)
	GPIO.output(relay_pump,GPIO.HIGH)
	GPIO.output(relay_power,GPIO.HIGH)

	log_event('Irigation turned off')

	if thread != None:
		thread.send_text('Irigation turned off')


#------------ Cron Scheduler ------------ 

nom_scheduler = BackgroundScheduler()

def compute_stop(start_h, start_m, dur_h, dur_m):
	stop_h = start_h + dur_h + (start_m + dur_m) / 60
	stop_m = (start_m + dur_m) % 60

	return stop_h, stop_m


#Summer lights
nom_scheduler.add_cron_job(lights_on, month = '4,5,6,7,8,9', hour = lights_sum_h, minute = lights_sum_m)

lights_sum_stop_h, lights_sum_stop_m = compute_stop(lights_sum_h, lights_sum_m, lights_dur_h, lights_dur_m)

nom.scheduler.add_cron_job(lights_off, month = '4,5,6,7,8,9', hour = lights_sum_stop_h, minute = lights_sum_stop_m)


#Winter lights
nom_scheduler.add_cron_job(lights_on, month = '1,2,3,10,11,12', hour = lights_win_h, minute = lights_win_m)

lights_win_stop_h, lights_win_stop_m = compute_stop(lights_win_h, lights_win_m, lights_dur_h, lights_dur_m)

nom.scheduler.add_cron_job(lights_off, month = '1,2,3,10,11,12', hour = lights_win_stop_h, minute = lights_win_stop_m)


#Irigation
nom_scheduler.add_cron_job(irigation_on, month = '4,5,6,7,8,9', hour = irigation_h, minute = irigation_m)

irigation_stop_h, irigation_stop_m = compute_stop(irigation_h, irigation_m, irigation_dur_h, irigation_dur_m)

nom_scheduler.add_cron_job(irigation_off, month = '4,5,6,7,8,9', hour = irigation_stop_h, minute = irigation_stop_m)


#Christmas Lights
nom_scheduler.add_cron_job(christmas_lights_on, month = '1,12', hour = lights_win_h, minute = lights_win_m)

lights_win_stop_h, lights_win_stop_m = compute_stop(lights_win_h, lights_win_m, lights_dur_h, lights_dur_m)

nom.scheduler.add_cron_job(lights_off, month = '1,2,3,10,11,12', hour = lights_win_stop_h, minute = lights_win_stop_m)


#Hourly Lights
for hour in range(0,6):
	nom_scheduler.add_cron_job(christmas_lights_on, hour = hour, minute = 0)
	nom_scheduler.add_cron_job(christmas_lights_on, hour = hour, minute = lights_hourly_dur_m)

nom_scheduler.print_jobs()
nom.scheduler.start()


#------------ Remote Commands ------------ 

ev_scheduler = BackgroundScheduler()

session = fbchat.Session.login(email, password)
listener = fbchat.Listener(session=session, chat_on=False, foreground=False)

verified_users = []

for event in listener.listen():
	if isinstance(event, fbchat.MessageEvent):
		
		if event.author.id != session.user.id:
			
			thread = event.thread

			if event.author not in verified_users:

				thread.send_text(hello_message)
				thread.send_emoji('😄', size=fbchat.EmojiSize.LARGE)
				time.sleep(1.5)
				thread.send_text(passwd_req)

				time.sleep(8)

				responses = thread.fetch_messages(limit = 1)

				for response in responses:

					if response.text != hello_message and response.text != passwd_req:	
						response.react('😍')
						if command_password == response.text:
								thread.send_text("Access Granted")
								verified_users.append(event.author)

								log_event('Added user' + str(event.author.id))
						else:
								thread.send_text("Acces Denied")

			else:

				message = event.message.text
				
				#compute command
				message = message.lower()
				print('Received command: ', message)

				split_message = message.split()

				command = -1
				for key in commands:
					if all(item in split_message for item in key.split()):
						command = commands.get(key)
						comm_key = key

				device = -1
				for key in devices:
					if all(item in split_message for item in key.lower().split()):
						device = devices.get(key)
						dev_key = key


				#Timing of command
				start_delay = 0
				run_time = default_run_time

				if 'in' in split_message:
					i = split_message.index('in')

					val = int(split_message[i+1])

					unit = split_message[i+2]

					if 'min' in unit:
						start_delay = val

					elif 'hour' in unit:
						start_delay = val * 60
					else:
						pass

				if 'for' in split_message:
					i = split_message.index('for')

					val = int(split_message[i+1])

					unit = split_message[i+2]

					if 'min' in unit:
						run_time = val
					elif 'hour' in unit:
						run_time = val * 60 
					else:
						pass

				if command != -1 and device != -1:
					
					thread.send_text(str(dev_key) + ' to ' + str(comm_key) + ' in ' + str(start_delay) + ' seconds for ' + str(run_time) + ' seconds.')

					current_time =  datetime.now()
					start_time = current_time + datetime.timedelta(0, start_delay * 60)
					stop_time = current_time + datetime.timedelta(0, (start_delay + run_time) *60 )
					
					ev_scheduler.add_date_job(turn_on, start_time, args = (thread,))
					ev.scheduler.add_date_job(turn_off, stops_time, args = (thread,))

					ev_scheduler.start()


				if command == 4:
					print('Delete all scheduled jobs')
					for job in ev_scheduler.get_jobs():
						job.remove()
					thread.send_text('Deleted all scheduled tasks.')


				if command == 3:
					print('Reporting Log file')

					try:
						with open(log_file) as log:
							for line in (log.readlines() [-N:]):
								thread.send_text(line, end = '')

					except:
						thread.send_text('No log file found.')


