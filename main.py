#NK

#TODO:
# rolling log files
# change this to a service: "service start/restart/stop/info": https://pypi.python.org/pypi/python-daemon/ CONSIDER HOW IT IS AUTOSTARTED, maybe start it from cron?


import logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler('/home/pi/shabbat/shabbat.log')
fileHandler.setLevel(logging.DEBUG)
#logging.basicConfig(filename='//home/pi/shabbat/shabbat.log', level=logging.DEBUG)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.DEBUG)
rootLogger.addHandler(consoleHandler)


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import datetime
import getopt
import glob
try:
	import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
import os
#import pyglet
#pyglet.lib.load_library('avbin')
#pyglet.have_avbin=True
from mutagen.mp3 import MP3
import pytz
from pytz import utc
import random
from subprocess import Popen, PIPE, STDOUT
import sys
import time
import times
from tendo import singleton
from  jewish_dates import holidays
from tzlocal import get_localzone


candlelight_delta = 20			# minutes before sunset
music_start_delta = 20			# Start music <x> minutes before candle-lighting
music_start_delay = 5			# Delay music <x> SECONDS after turning on power
music_finish_delta = 2			# Finish music <x> minutes before candle-lighting
#music_base_path = r'C:\Users\nadavk\Music'
music_base_path = r'/home/pi/ShabbatMusic'
location = 'Azriel_wiki'
#location = 'Raanana_wiki'
GPIOchannel = 12


class player_data:

	def __init__(self, candlelight, music_start, folders):
		self.candlelight = candlelight
		self.music_start = music_start
		self.folders = folders
		
	def __str__(self):
		#return ', '.join("%s: %s" % item for item in vars(self).items())
		#return ', '.join("%s: %s" % (str(name), str(val)) for (name, val) in vars(self).items())
		s = ''
		for (name, val) in vars(self).items():
			if val is not None:
				s += str(name) + ":" + str(val) + ", "
		return s
		#return str(self.__dict__)
		

def init_elec():
	try:
		GPIO.setwarnings(False)		# https://raspberrypi.stackexchange.com/questions/55143/gpio-warning-channel-already-in-use
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(GPIOchannel, GPIO.OUT, initial=GPIO.LOW)
	except:
		logging.exception('ERROR: init_elec')


def set_elec(state):
	try:
		GPIO.output(GPIOchannel, state)
	except:
		logging.exception('ERROR: set_elec_gpio')


def get_random_file(path):
	files = glob.glob(path)
	return random.choice(files) if files else None


def find_mp3_file(base_folder, folders, sub_folder):
	for folder in folders:
		path = os.path.join(base_folder, folder, sub_folder)
		#file = get_random_file(os.path.join(path, '*.mp3'))
		file = get_random_file(os.path.join(path, '*.*'))
		if file:
			file = os.path.join(path, file)
			
			#if sys.stdout.encoding != 'cp850':
			#  sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'strict')
			#if sys.stderr.encoding != 'cp850':
			#  sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'strict')
			
			#print('Found file: ', file)
			try:
				#logging.debug('Found file: %s', file.encode(encoding='mbcs'))
				logging.debug('Found file: %s', file)
			except:
				logging.exception('ERROR: Music files must be in English: %s', file)
				return
			
			return file #.encode(encoding=sys.getfilesystemencoding())
	else:	#no file found
		logging.error('File not found in these paths (\'/%s\'): %s', sub_folder, folders)


def play_music_file(file):
	"""
	Starts playing the file and returns a player object
	"""
	#return Popen(['mpg321', '--gain', '100', file], stdout=PIPE, stderr=STDOUT, close_fds=True)
	return Popen(['omxplayer', '-o', 'local', '--no-keys', '--vol', '0', file], stdout=PIPE, stderr=STDOUT, close_fds=True)


def get_music_file_duration(file):
	return MP3(file).info.length


def stop_music_file(player):
	try:
		player.terminate()
		player.kill()
		player.stdout.close()
		player.stderr.close()
		player.stdin.close()
	except:
		pass
	player = None

	
def stop_music_1(data):
	logging.info('Stopping player 1')
	
	if hasattr(data, 'player1'):
		try:
			#data.player1.pause()
			stop_music_file(data.player1)
			logging.info('player1 stopped')
		except:
			logging.exception('player1 stop raised exception')
		

def stop_music_2(data):
	logging.info('Stopping player 2')
	if hasattr(data, 'player2'):
		try:
			#data.player2.pause()
			stop_music_file(data.player2)
			logging.info('player2 stopped')
		except:
			logging.exception('player2 stop raised exception')


def stop_music(scheduler=None, data=None):
	logging.info('Closing elec')
	set_elec(False)

	if data:
		logging.info('Stopping players')
		stop_music_1(data)
		stop_music_2(data)

	# after playing music we shutdown. cron job should start new instance
	sys.exit()

	
def play_music_2(scheduler, data):
	logging.info('Music time 2: %s', str(data))
	stop_music_1(data)
	
	#data.player2 = data.source2.play()
	#data.player2.volume = 1.0		#1.0 is max
	data.player2 = play_music_file(data.file2)


def play_music_1(scheduler, data, just_1_test=False):
	logging.info('Turning on elec')
	set_elec(True)
	logging.debug('Waiting {0} seconds'.format(music_start_delay))
	time.sleep(music_start_delay)

	if not hasattr(data, 'player1') or not data.file1:
		data.file1 = find_mp3_file(music_base_path, data.folders, '1')
	logging.info('Music A: %s', str(data))
	if data.file1:
		data.duration1 = get_music_file_duration(data.file1)
		
		#data.player1 = data.source1.play()
		#data.player1.volume = 1.0		#1.0 is max
		data.player1 = play_music_file(data.file1)
		
		logging.info('Music B: %s', str(data))
		if just_1_test:
			#pyglet.app.run()		requires Open-GL
			time.sleep(int(data.duration1))
			return
	else:  # no file found
		logging.error('File 1 not found in these paths: %s', data.folders)
		if just_1_test:
			return


	data.file2 = find_mp3_file(music_base_path, data.folders, '2')
	if data.file2:
		data.duration2 = get_music_file_duration(data.file2)

		data.music_start_2 = data.candlelight - datetime.timedelta(minutes=music_finish_delta, seconds=data.duration2)
		logging.info('Music C: %s', str(data))

		logging.debug('Start_music 2 (-{0}, -{1}): {2} : '.format(music_finish_delta, data.duration2, data.music_start_2))
		if scheduler:
			scheduler.add_job(play_music_2, 'date', run_date=data.music_start_2, misfire_grace_time=2, args=[scheduler, data])
			scheduler.print_jobs()
	else:  # no file found
		logging.error('File 2 not found in these paths: %s', data.folders)


def set_shabbat_job(scheduler):
	sunset = times.today_sunrise_sunset(location)[1]
	candlelight = sunset - datetime.timedelta(minutes=candlelight_delta)
	music_start = candlelight - datetime.timedelta(minutes=music_start_delta)

	#shabbat = datetime(2015, 2, 9, 22, 56, 30)
	
	print ('Sunset: ', sunset)
	print ('Candlelight (-{0}): {1}'.format(candlelight_delta, candlelight))
	print ('Start_music 1 (-{0}): {1} : '.format(music_start_delta, music_start))
	
	
	data = player_data(candlelight, music_start, folders=holidays.get_music_folders())

	
	#scheduler.add_job(play_music_1, 'date', run_date=music_start, misfire_grace_time=2, timezone=utc)
	scheduler.add_job(play_music_1, 'date', run_date=music_start, misfire_grace_time=2, args=[scheduler, data])
	scheduler.add_job(stop_music, 'date', run_date=data.candlelight, misfire_grace_time=2, args=[scheduler, data])
	scheduler.print_jobs()


def daily_check(scheduler):
	# tz = get_localzone()
	# local_dt = tz.localize(datetime.now(), is_dst=None)
	# utc_dt = local_dt.astimezone(utc) #NOTE: utc.normalize() is unnecessary here	
	# print ('local: ', local_dt)
	# print('utc1:', utc_dt)
	# print('utc2:', datetime.now(pytz.timezone("utc")))
	# print('utc3:', datetime.now(utc))
	#now_utc = datetime.now(utc)
	#print('holiday: ', holidays.calculate_holiday(now_utc.day, now_utc.month, now_utc.year, diaspora=False))
	today = datetime.date.today()
	if today.year > 2014 and holidays.play_music_today(today):
		logging.debug('Today is a holiday')
		set_shabbat_job(scheduler)


def main(argv):
	# set high priority
	# Remarked 2019-07-19
	# os.nice(-20)
	# os.setpriority(os.PRIO_PROCESS, 0, -20)
	# import psutil
	# p = psutil.Process()
	# p.ionice(0)

	logging.info("Shabbat-times started")

	try:
		try:
			opts, args = getopt.getopt(argv, "htp:", ["test=", "play="])
		except getopt.GetoptError:
			print('main.py --test=<year> -play')
			sys.exit(2)
		for opt, arg in opts:
			if opt == '-h':
				print('main.py --test=<year> -play')
				sys.exit()
			elif opt in ("-t", "-test", "--test"):
				year = arg
				logging.info('TEST')
				print('Shabbat Times:')
				#for t in times.shabbat_times(location, 55, candlelight_delta):
				#	print (t)
				print('Music Folders for year:', int(year))
				print(holidays.test_music_folders(int(year)))
				sys.exit()
			elif opt in ("-p", "-play", "--play"):
				print('Playing')
				init_elec()
				data = player_data(candlelight=None, music_start=None, folders=['Shabbat'])

				file = arg
				if file:
					data.file1 = file

				play_music_1(None, data, just_1_test=True)
				print('Played')
				sys.exit()


		# ensure single instance process
		me = singleton.SingleInstance()

		if os.getuid() != 0:
			logging.warn('Consider running as sudo')
			print('Consider running as sudo')

		init_elec()

		today_sunrise_sunset = times.today_sunrise_sunset(location)
		logging.debug('today suntimes: %s, %s', today_sunrise_sunset[0], today_sunrise_sunset[1])
		print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))


		loop = asyncio.get_event_loop()

		#scheduler = AsyncIOScheduler(timezone=utc, standalone=False)
		scheduler = BackgroundScheduler(timezone=get_localzone(), standalone=False)
		
		#Daily reset job
		#scheduler.add_job(daily_check, 'cron', hour='3', minute='0', args=[scheduler])
		scheduler.add_job(daily_check, 'cron', hour='0', minute='1', args=[scheduler])
		scheduler.start()
		scheduler.print_jobs()

		daily_check(scheduler)		#check the times for today

		
		# # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
		# try:
			# asyncio.get_event_loop().run_forever()
		# except (KeyboardInterrupt, SystemExit):
			# pass	

		logging.debug('waiting...')	
		
		loop.run_forever()
		loop.close()
		scheduler.shutdown(wait=False)
		
	except Exception:
		logging.exception('unhandled exception')
	except SystemExit:
		logging.debug('System Exiting')


if __name__ == '__main__':
	try:
		main(sys.argv[1:])
	except:
		logging.exception('main exception caught')
	logging.info('Exiting main')
	stop_music()
