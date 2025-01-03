from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from weather import Weather, Unit

def talkToMe(audio):
	"speaks audio passed as argument"

	print(audio)
	for line in audio.splitlines():
		os.system("say " + audio)

	text_to_speech=gTTS(text=audio, lang='en-uk')


def myCommand():

	"listens for commands"

	r = sr.Recognizer()

	with sr.Microphone() as source:
		print('I am ready for your next command')
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
	
		try:
			r.start_threshold = 1
			command = r.recognize_google(audio)
			print('You said: ' + command + '\n')

		except sr.UnknownValueError:
			print('Your last command couldn\'t be heard')
			command = myCommand();
			
		return command

def assistant(command):
	"if statements for executing commands"

	if 'open realm' in command:
		talkToMe('opening realm of the mad god')
		reg_ex = re.search('open realm (.*)', command)
		url = 'https://www.realmofthemadgod.com/'
		if reg_ex:
			subreddit = reg_ex.group(1)
			url = url + 'r/' + subreddit
		webbrowser.open(url)
		print('Done!')

	elif 'go to' in command:
		talkToMe('as you wish')
		reg_ex = re.search('go to (.+)', command)
		if reg_ex:
			domain = reg_ex.group(1)
			url = 'https://www.' + domain
			webbrowser.open(url)
			print('Done!')
		else:
			pass

	elif 'how are you' in command:
		talkToMe('good if you are good')
	elif 'joke' in command:
		talkToMe('alright')
		res = requests.get(
				'https://icanhazdadjoke.com/',
				headers={"Accept":"application/json"}
		)
		if res.status_code == requests.codes.ok:
			talkToMe(str(res.json()['joke']))
		else:
			talkToMe('oops! I ran out of jokes')

	elif 'current weather in' in command:
		talkToMe('as you wish')
		reg_ex = re.search('current weather in (.*)', command)
		if reg_ex:
			city = reg_ex.group(1)
			weather = Weather(unit=Unit.CELSIUS)
			location = weather.lookup_by_location(city)
			condition = location.condition
			talkToMe('The current weather in %s is %s. The temperature is %s degrees.' % (city, condition.text, condition.temp))

	elif 'weather forecast in' in command:
		talkToMe('as you wish')
		reg_ex = re.search('weather forecast in (.*)', command)
		if reg_ex:
			city = reg_ex.group(1)
			weather = Weather(unit=Unit.CELSIUS)
			location = weather.lookup_by_location(city)
			forecasts = location.forecast
			for i in range(0, 3):
				talkToMe('On %s, weather is %s. The high will be %u degree. The low will be %u degrees.' %
						 (forecasts[i].date, forecasts[i].text, (int)(forecasts[i].high),
						 (int)(forecasts[i].low)))


	elif 'email' in command:
		talkToMe('whom shall i email?')
		
		recipient = myCommand()

		talkToMe('with what subject?')
		subject = myCommand()
		
		talkToMe('what should I say?')
		content = myCommand()
		
		if 'myself' in recipient:
  
			talkToMe('Sending to Howard Wang')

			fromaddr = "luw055@ucsd.edu"

			toaddr = "luw055@ucsd.edu"
			
			msg = MIMEMultipart()

			msg['From'] = fromaddr

			msg['To'] = toaddr

			msg['Subject'] = subject

			msg.attach(MIMEText(content, 'plain'))
			
			text = msg.as_string()

			mail = smtplib.SMTP('smtp.gmail.com', 587)
			mail.starttls()
			mail.login(fromaddr, '28@r289')
			mail.sendmail(fromaddr, toaddr, text)
			mail.quit()

			talkToMe('Email sent.')

		elif 'father' in recipient:
		 
			talkToMe('Sending to Terry Wang')

			fromaddr = "luw055@ucsd.edu"

			toaddr = "terry.tiancai@gmail.com"
			
			msg = MIMEMultipart()

			msg['From'] = fromaddr

			msg['To'] = toaddr

			msg['Subject'] = subject

			msg.attach(MIMEText(content, 'plain'))
			
			text = msg.as_string()

			mail = smtplib.SMTP('smtp.gmail.com', 587)
			mail.starttls()
			mail.login(fromaddr, '28@r289')
			mail.sendmail(fromaddr, toaddr, text)
			mail.quit()

			talkToMe('Email sent.')
	
		elif 'doris' in recipient:
		 
			talkToMe('Sending to Doris Liu')

			fromaddr = "luw055@ucsd.edu"

			toaddr = "dol121@ucsd.edu"
			
			msg = MIMEMultipart()

			msg['From'] = fromaddr

			msg['To'] = toaddr

			msg['Subject'] = subject

			msg.attach(MIMEText(content, 'plain'))
			
			text = msg.as_string()

			mail = smtplib.SMTP('smtp.gmail.com', 587)
			mail.starttls()
			mail.login(fromaddr, '28@r289')
			mail.sendmail(fromaddr, toaddr, text)
			mail.quit()

			talkToMe('Email sent.')
	
		else:
			talkToMe('I dont know what you mean!')
	
	else:
		talkToMe('I dont know')

talkToMe('Hi Im Alpha! Welcome back!')

while True:
	assistant(myCommand())
	talkToMe('what is your next command?')


