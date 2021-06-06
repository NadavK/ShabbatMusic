#NK

#from jewish_dates.sun import GetSunrise, GetSunset
import astral.astral
import datetime
from tzlocal import get_localzone
from pytz import utc

#per http://www.yeshiva.co/calendar/, for Ra'anana, the most exact is Astral, with co-ords from Wiki, and -20 minutes

TZ = 0

astral.astral._LOCATION_INFO="""Raanana_wiki,Israel,32°11'N,34°52'E,Asia/Jerusalem,48
	Raanana_google,Israel,32.18N,34.87E,Asia/Jerusalem,44"""

def astral_location(location):
	a = astral.astral.Astral(astral.astral.AstralGeocoder)
	geo = a.geocoder
	return geo[location]

def get_google_geo():
	#Use this to get google co-ords and elevation
	from astral.astral import GoogleGeocoder
	a = astral.astral.Astral(astral.astral.GoogleGeocoder)
	geo = a.geocoder
	loc = geo['Tel-Aviv']
	print(loc, loc.elevation)
	
def next_friday(date):
	#returns closest fri, or next fri if today is fri
	#http://stackoverflow.com/questions/8801084/how-to-calculate-next-friday-in-python
	friday = 4	# 0 based, starting from Monday
	return date + datetime.timedelta( ((friday-1) - date.weekday()) % 7 + 1)

def this_friday(date):
	#returns closest fri, and return today if today is fri
	#http://stackoverflow.com/questions/8801084/how-to-calculate-next-friday-in-python
	friday = 4	# 0 based, starting from Monday
	return date + datetime.timedelta( (friday - date.weekday()) % 7)

def sunrise_sunset_jd(location, date):
	#latitude, longitude, timezone, elevation
	sunrise = GetSunrise(uMonth=date.month, uDay=date.day, uYear=date.year, location=location)
	sunset = GetSunset(uMonth=date.month, uDay=date.day, uYear=date.year, location=location)
	sunrise_date = date + datetime.timedelta(hours=sunrise[0], minutes=sunrise[1])
	sunset_date = date + datetime.timedelta(hours=sunset[0], minutes=sunset[1])
	return sunrise_date, sunset_date

def today_sunrise_sunset_jd(location):
	return sunrise_sunset(location=location, date=datetime.datetime.today())


def sunrise_sunset_astral(location, date):
	#local False for UTC
	astral = astral_location(location)
	return astral.sun(local=False, date=date)

def today_sunrise_sunset_astral(location):
	return sunrise_sunset_astral(location=location, date=datetime.date.today())

	
def sunrise_sunset(location, date):
	a = astral.astral.Astral(astral.astral.AstralGeocoder)
	geo = a.geocoder
	sun = sunrise_sunset_astral(location=location, date=date)
	
	sunrise_utc = sun['sunrise'].replace(tzinfo=utc)		#aastral times are utc, this is just for explicity
	sunset_utc = sun['sunset'].replace(tzinfo=utc)

	local_tz = get_localzone()
	# Convert time zone
	sunrise_local = sunrise_utc.astimezone(local_tz)
	sunset_local = sunset_utc.astimezone(local_tz)
	
	return (sunrise_local, sunset_local)
	
def today_sunrise_sunset(location):
	return sunrise_sunset(location, datetime.date.today())
	
def shabbat_start(location, date, candlelight_delta):
	return sunrise_sunset(location, date)[1] - datetime.timedelta(minutes=candlelight_delta)
	
def this_shabbat_start():
	fri = this_friday(datetime.datetime.today())
	return shabbat_start(fri)

def shabbat_times(location, num, candlelight_delta):
	#returns the next <num> shabbat times

	#a = astral.astral.Astral(astral.astral.AstralGeocoder)
	#geo = a.geocoder
	
	times=[]

	fri = datetime.datetime.today()
	for i in range(1,num):
		fri = next_friday(fri)
		#print ('raanana_wiki  ', sunrise_sunset_jd(locations['raanana_wiki'], fri)[1] - datetime.timedelta(minutes=candlelight))
		#print ('raanana_google', sunrise_sunset_jd(locations['raanana_google'], fri)[1] - datetime.timedelta(minutes=candlelight))
		#print ('*Raanana_wiki  ', sunrise_sunset_astral(geo['Raanana_wiki'], fri)['sunset'] - datetime.timedelta(minutes=candlelight))
		#print ('Raanana_google', sunrise_sunset_astral(geo['Raanana_google'], fri)['sunset'] - datetime.timedelta(minutes=candlelight))
		#times.append(sunrise_sunset(fri)[1] - datetime.timedelta(minutes=candlelight))
		times.append(shabbat_start(location, fri, candlelight_delta))
	return times
