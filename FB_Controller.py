#https://github.com/carpedm20/fbchat

import fbchat
import time
import sys
import RPi.GPIO as GPIO    
import sched

scheduler = sched.scheduler(time.time, time.sleep)


#Lights Relay

relay_power = 2
relay_lights = 3

#Setting up GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(relay_power,GPIO.OUT)
GPIO.output(relay_power,GPIO.HIGH)

GPIO.setup(relay_lights,GPIO.OUT)
GPIO.output(relay_lights,GPIO.HIGH)


def turn_on(thread):
	print('Turned on:', time.time())
	thread.send_text("Lights turned on")

	f = open(log_file,"a")
	f.write("Turned lighs on at " + str(time.time()))
	f.close()

	GPIO.output(relay_lights,GPIO.LOW)
	GPIO.output(relay_power,GPIO.LOW)

def turn_off(thread):
	print('Turned off:', time.time())
	thread.send_text("Lights turned off")

	f = open(log_file,"a")
	f.write("Turned lighs off at " + str(time.time()))
	f.close()

	GPIO.output(relay_lights,GPIO.HIGH)
	GPIO.output(relay_power,GPIO.HIGH)


#Bot credentials
email = "tdrvlad@gmail.com"
password = "12345678901234567890"

command_password = "****"

#Definitions

log_file = 'Log.txt'

default_run_time = 10 #minutes

#Principal commands
commands = {'turn on' : 1, 'turn off' : 0, 'check' : 2, 'report' : 3, 'clear command' : 4}

#Alternative ways of expressing principal commands
alt_commands = {'start' : 1, 'stop' : 0, 'delete command' : 4}

#principal controlled devices
devices = {'Lights' : 1}

#Alternative ways of naming controlled devices
alt_devices = {'illumination' : 1}


#Updating the dictionaries
commands.update(alt_commands)
devices.update(alt_devices)


session = fbchat.Session.login(email, password)
listener = fbchat.Listener(session=session, chat_on=False, foreground=False)

verified_users = []

hello_message = 'Hello!'
passwd_req = 'Please, type the password'
for event in listener.listen():
	if isinstance(event, fbchat.MessageEvent):
		
		if event.author.id != session.user.id:
			
			thread = event.thread

			if event.author not in verified_users:

				thread.send_text(hello_message)
				thread.send_emoji('😄', size=fbchat.EmojiSize.LARGE)
				time.sleep(1.5)
				thread.send_text(passwd_req)

				time.sleep(7)

				responses = thread.fetch_messages(limit = 1)

				for response in responses:

					if response.text != hello_message and response.text != passwd_req:	
						response.react('😍')
						if command_password == response.text:
								thread.send_text("Access Granted")
								verified_users.append(event.author)

								f = open(log_file,"w")
								f.write("Added user " + str(event.author.id))
								f.close()
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
				run_time = default_run_time * 60

				if 'in' in split_message:
					i = split_message.index('in')

					val = int(split_message[i+1])

					unit = split_message[i+2]

					if 'min' in unit:
						start_delay = val * 60

					elif 'hour' in unit:
						start_delay = val * 60 * 60
					else:
						pass

				if 'for' in split_message:
					i = split_message.index('for')

					val = int(split_message[i+1])

					unit = split_message[i+2]

					if 'min' in unit:
						run_time = val * 60

					elif 'hour' in unit:
						run_time = val * 60 * 60
					else:
						pass

				
				if command != -1 and device != -1:
					
					thread.send_text(str(dev_key) + ' to ' + str(comm_key) + ' in ' + str(start_delay) + ' seconds for ' + str(run_time) + ' seconds.')

					#Define task scheduler
					
					scheduler.enter(start_delay, 1, turn_on, (thread,))
					scheduler.enter(start_delay + run_time, 1, turn_off, (thread,))

					scheduler.run()


				if command == 4:
					print('Delete all future events')
					for event in scheduler.queue:
						scheduler.cancel(event)

				if command == 3:
					print('Reporting Log file')
					log = open(log_file, 'r').read()
					thread.send_text(log)
	



			







