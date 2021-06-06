#http://www.david-greve.de/luach-code/jewish-python.html
import datetime
import date_utils.calendar_util
import collections
from jewish_dates.parasha import getTorahSections

# Returns the weekday from a given hebrew date (0 for Sunday, 1 for Monday,...)
def getWeekdayOfHebrewDate(hebDay, hebMonth, hebYear):
  # Calculating the julian date
  julian = date_utils.calendar_util.hebrew_to_jd(hebYear, hebMonth, hebDay)
  weekday = (int(julian) + 2) % 7
  return weekday

def calculate_holiday(g_day, g_month, g_year, diaspora=False):
  julian = date_utils.calendar_util.gregorian_to_jd(g_year, g_month, g_day)
  hebYear, hebMonth, hebDay = date_utils.calendar_util.jd_to_hebrew(julian)

  listHolidays = []

  # Holidays in Nisan

  hagadolDay = 14
  while getWeekdayOfHebrewDate(hagadolDay, 1, hebYear) != 6:
    hagadolDay -= 1
  if hebDay == hagadolDay and hebMonth == 1:
    listHolidays.append("Shabat Hagadol")

  if hebDay == 14 and hebMonth == 1:
    listHolidays.append("Erev Pesach")
  if hebDay == 15 and hebMonth == 1:
    listHolidays.append("Pesach I")
  if hebDay == 16 and hebMonth == 1:
    if diaspora:
      listHolidays.append("Pesach II")
    else:
      listHolidays.append("Chol Hamoed")
  if hebDay == 17 and hebMonth == 1:
    listHolidays.append("Chol Hamoed")
  if hebDay == 18 and hebMonth == 1:
    listHolidays.append("Chol Hamoed")
  if hebDay == 19 and hebMonth == 1:
    listHolidays.append("Chol Hamoed")
  if hebDay == 20 and hebMonth == 1:
    listHolidays.append("Chol Hamoed")
  if hebDay == 21 and hebMonth == 1:
    if not diaspora:
      listHolidays.append("Pesach VII (Yizkor)")
    else:
      listHolidays.append("Pesach VII")
  if hebDay == 22 and hebMonth == 1:
    if diaspora:
      listHolidays.append("Pesach VIII (Yizkor)")

  # Yom Hashoah

  if getWeekdayOfHebrewDate(27, 1, hebYear) == 5:
    if hebDay == 26 and hebMonth == 1:
      listHolidays.append("Yom Hashoah")
  elif hebYear >= 5757 and getWeekdayOfHebrewDate(27, 1, hebYear) == 0:
    if hebDay == 28 and hebMonth == 1:
      listHolidays.append("Yom Hashoah")
  else:
    if hebDay == 27 and hebMonth == 1:
      listHolidays.append("Yom Hashoah")

  # Holidays in Iyar

  # Yom Hazikaron

  if getWeekdayOfHebrewDate(4, 2, hebYear) == 5: # If 4th of Iyar is a Thursday ...
    if hebDay == 2 and hebMonth == 2: # ... then Yom Hazicaron is on 2th of Iyar
      listHolidays.append("Yom Hazikaron")
  elif getWeekdayOfHebrewDate(4, 2, hebYear) == 4:
    if hebDay == 3 and hebMonth == 2:
        listHolidays.append("Yom Hazikaron")
  elif hebYear >= 5764 and getWeekdayOfHebrewDate(4, 2, hebYear) == 0:
    if hebDay == 5 and hebMonth == 2:
      listHolidays.append("Yom Hazikaron")
  else:
    if hebDay == 4 and hebMonth == 2:
      listHolidays.append("Yom Hazikaron")

  # Yom Ha'Azmaut

  if getWeekdayOfHebrewDate(5, 2, hebYear) == 6:
    if hebDay == 3 and hebMonth == 2:
      listHolidays.append("Yom Ha'Atzmaut")
  elif getWeekdayOfHebrewDate(5, 2, hebYear) == 5:
    if hebDay == 4 and hebMonth == 2:
      listHolidays.append("Yom Ha'Atzmaut")
  elif hebYear >= 5764 and getWeekdayOfHebrewDate(4, 2, hebYear) == 0:
    if hebDay == 6 and hebMonth == 2:
      listHolidays.append("Yom Ha'Atzmaut")
  else:
    if hebDay == 5 and hebMonth == 2:
      listHolidays.append("Yom Ha'Atzmaut")

  if hebDay == 14 and hebMonth == 2:
    listHolidays.append("Pesach Sheni")
  if hebDay == 18 and hebMonth == 2:
    listHolidays.append("Lag B'Omer")
  if hebDay == 28 and hebMonth == 2:
    listHolidays.append("Yom Yerushalayim")

  # Holidays in Sivan

  if hebDay == 5 and hebMonth == 3:
    listHolidays.append("Erev Shavuot")
  if hebDay == 6 and hebMonth == 3:
    if diaspora:
      listHolidays.append("Shavuot I")
    else:
      listHolidays.append("Shavuot\n(Yizkor)")
  if hebDay == 7 and hebMonth == 3:
    if diaspora:
      listHolidays.append("Shavuot II\n(Yizkor)")

  # Holidays in Tammuz

  if getWeekdayOfHebrewDate(17, 4, hebYear) == 6:
    if hebDay == 18 and hebMonth == 4:
      listHolidays.append("Fast of Tammuz")
  else:
    if hebDay == 17 and hebMonth == 4:
      listHolidays.append("Fast of Tammuz")

  # Holidays in Av

  if getWeekdayOfHebrewDate(9, 5, hebYear) == 6:
    if hebDay == 10 and hebMonth == 5:
      listHolidays.append("Fast of Av")
  else:
    if hebDay == 9 and hebMonth == 5:
      listHolidays.append("Fast of Av")
  if hebDay == 15 and hebMonth == 5:
    listHolidays.append("Tu B'Av")

  # Holidays in Elul

  if hebDay == 29 and hebMonth == 6:
    listHolidays.append("Erev Rosh Hashana")

  # Holidays in Tishri

  if hebDay == 1 and hebMonth == 7:
    listHolidays.append("Rosh Hashana I")
  if hebDay == 2 and hebMonth == 7:
    listHolidays.append("Rosh Hashana II")
  if getWeekdayOfHebrewDate(3, 7, hebYear) == 6:
    if hebDay == 4 and hebMonth == 7:
      listHolidays.append("Tzom Gedaliah")
  else:
    if hebDay == 3 and hebMonth == 7:
      listHolidays.append("Tzom Gedaliah")
  if hebDay == 9 and hebMonth == 7:
    listHolidays.append("Erev Yom Kippur")
  if hebDay == 10 and hebMonth == 7:
    listHolidays.append("Yom Kippur\n(Yizkor)")
  if hebDay == 14 and hebMonth == 7:
    listHolidays.append("Erev Sukkot")
  if hebDay == 15 and hebMonth == 7:
    if diaspora:
      listHolidays.append("Sukkot I")
    else:
      listHolidays.append("Sukkot")
  if hebDay == 16 and hebMonth == 7:
    if diaspora:
      listHolidays.append("Sukkot II")
    else:
      listHolidays.append("Chol Hamoed")
  if hebDay == 17 and hebMonth == 7:
    listHolidays.append("Chol Hamoed")
  if hebDay == 18 and hebMonth == 7:
    listHolidays.append("Chol Hamoed")
  if hebDay == 19 and hebMonth == 7:
    listHolidays.append("Chol Hamoed")
  if hebDay == 20 and hebMonth == 7:
    listHolidays.append("Chol Hamoed")
  if hebDay == 21 and hebMonth == 7:
    listHolidays.append("Hoshana Raba")
  if hebDay == 22 and hebMonth == 7:
    if not diaspora:
      listHolidays.append("Shemini Atzereth\n(Yizkor)")
      listHolidays.append("Simchat Torah")
    else:
      listHolidays.append("Shemini Atzereth\n(Yizkor)")
  if hebDay == 23 and hebMonth == 7:
    if diaspora:
      listHolidays.append("Simchat Torah")

  # Holidays in Kislev

  if hebDay == 25 and hebMonth == 9:
    listHolidays.append("Chanukka I")
  if hebDay == 26 and hebMonth == 9:
    listHolidays.append("Chanukka II")
  if hebDay == 27 and hebMonth == 9:
    listHolidays.append("Chanukka III")
  if hebDay == 28 and hebMonth == 9:
    listHolidays.append("Chanukka IV")
  if hebDay == 29 and hebMonth == 9:
    listHolidays.append("Chanukka V")
  # Holidays in Tevet

  if hebDay == 10 and hebMonth == 10:
    listHolidays.append("Fast of Tevet")

  if date_utils.calendar_util.hebrew_month_days(hebYear, 9) == 30:
    if hebDay == 30 and hebMonth == 9:
      listHolidays.append("Chanukka VI")
    if hebDay == 1 and hebMonth == 10:
      listHolidays.append("Chanukka VII")
    if hebDay == 2 and hebMonth == 10:
      listHolidays.append("Chanukka VIII")
  if date_utils.calendar_util.hebrew_month_days(hebYear, 9) == 29:
    if hebDay == 1 and hebMonth == 10:
      listHolidays.append("Chanukka VI")
    if hebDay == 2 and hebMonth == 10:
      listHolidays.append("Chanukka VII")
    if hebDay == 3 and hebMonth == 10:
      listHolidays.append("Chanukka VIII")

  # Holidays in Shevat

  if hebDay == 15 and hebMonth == 11:
    listHolidays.append("Tu B'Shevat")

  # Holidays in Adar (I)/Adar II

  if date_utils.calendar_util.hebrew_leap(hebYear):
    monthEsther = 13
  else:
    monthEsther = 12

  if getWeekdayOfHebrewDate(13, monthEsther, hebYear) == 6:
    if hebDay == 11 and hebMonth == monthEsther:
      listHolidays.append("Fast of Esther")
  else:
    if hebDay == 13 and hebMonth == monthEsther:
      listHolidays.append("Fast of Esther")

  if hebDay == 14 and hebMonth == monthEsther:
    listHolidays.append("Purim")
  if hebDay == 15 and hebMonth == monthEsther:
    listHolidays.append("Shushan Purim")

  if date_utils.calendar_util.hebrew_leap(hebYear):
    if hebDay == 14 and hebMonth == 12:
      listHolidays.append("Purim Katan")
    if hebDay == 15 and hebMonth == 12:
      listHolidays.append("Shushan Purim Katan")

  return listHolidays



def get_erev_hag(g_day, g_month, g_year, diaspora=False):
  #Returns Erev Hag, and then the name of the Hag

  julian = date_utils.calendar_util.gregorian_to_jd(g_year, g_month, g_day)
  hebYear, hebMonth, hebDay = date_utils.calendar_util.jd_to_hebrew(julian)
  #print('get_erev_hag={0}/{1}/{2} --> {3} --> {4}/{5}/{6}'.format(g_year, g_month, g_day, julian, hebYear, hebMonth, hebDay))

  if getWeekdayOfHebrewDate(hebDay, hebMonth, hebYear) == 6: # No music on Shabbat...
    return None

  # Holidays in Nisan
  if hebDay == 14 and hebMonth == 1:
    return "Pesach"
  if hebDay == 20 and hebMonth == 1:
    return "Pesach"

  # Holidays in Sivan
  if hebDay == 5 and hebMonth == 3:
    return "Shavuot"

  # Holidays in Elul
  if hebDay == 29 and hebMonth == 6:
    return "Rosh Hashana"
  if hebDay == 1 and hebMonth == 7:
    return "Rosh Hashana"

  # Holidays in Tishri
  if hebDay == 9 and hebMonth == 7:
    return "Yom Kippur"
  if hebDay == 14 and hebMonth == 7:
    return "Sukkot"
  if hebDay == 21 and hebMonth == 7:
    return "Simchat Torah"


def get_holiday(g_day, g_month, g_year, diaspora=False):
  #returns the name of the holiday, but only if that holiday is not a hag (not a holiday that plays music for itself)
  #but return a hag erev hag is Motsash/ag on Sunday (since it will not play music)
  #also, the holiday is a general name (not Pesach II, just Pesach)
  julian = date_utils.calendar_util.gregorian_to_jd(g_year, g_month, g_day)
  hebYear, hebMonth, hebDay = date_utils.calendar_util.jd_to_hebrew(julian)

  is_friday = getWeekdayOfHebrewDate(hebDay, hebMonth, hebYear) == 6	#play on shabbat hol-hamoed, but not the shabbat before hag.
  is_sunday = getWeekdayOfHebrewDate(hebDay, hebMonth, hebYear) == 0	#if hag is on sunday, play the special music on shabbat
  
  # Holidays in Nisan
  if hebDay == 15 and hebMonth == 1 and is_sunday:
    return ({0: "Pesach", 1: "Hag"})
  if hebDay == 16 and hebMonth == 1 and is_friday:
    return ({0: "Pesach"})
  if hebDay == 17 and hebMonth == 1 and is_friday:
    return ({0: "Pesach"})
  if hebDay == 18 and hebMonth == 1 and is_friday:
    return ({0: "Pesach"})
  if hebDay == 19 and hebMonth == 1 and is_friday:
    return ({0: "Pesach"})
  if hebDay == 20 and hebMonth == 1 and is_friday:
    return ({0: "Pesach"})
  #if hebDay == 21 and hebMonth == 1:
  #    return ({0: "Pesach"})
  #if hebDay == 22 and hebMonth == 1 and diaspora:
  #    return ({0: "Pesach"})

  # Yom Hashoah
  if getWeekdayOfHebrewDate(27, 1, hebYear) == 5:
    if hebDay == 26 and hebMonth == 1:
      return ({0: "Yom Hashoah"})
  elif hebYear >= 5757 and getWeekdayOfHebrewDate(27, 1, hebYear) == 0:
    if hebDay == 28 and hebMonth == 1:
      return ({0: "Yom Hashoah"})
  else:
    if hebDay == 27 and hebMonth == 1:
      return ({0: "Yom Hashoah"})

  # Holidays in Iyar

  # Yom Hazikaron
  if getWeekdayOfHebrewDate(4, 2, hebYear) == 5: # If 4th of Iyar is a Thursday ...
    if hebDay == 2 and hebMonth == 2: # ... then Yom Hazikaron is on 2th of Iyar
      return ({2: "Yom Hazikaron"})
  elif getWeekdayOfHebrewDate(4, 2, hebYear) == 4:
    if hebDay == 3 and hebMonth == 2:
        return ({2: "Yom Hazikaron"})
  elif hebYear >= 5764 and getWeekdayOfHebrewDate(4, 2, hebYear) == 0:
    if hebDay == 5 and hebMonth == 2:
      return ({2: "Yom Hazikaron"})
  else:
    if hebDay == 4 and hebMonth == 2:
      return ({2: "Yom Hazikaron"})

  # Yom Ha'Azmaut
  if getWeekdayOfHebrewDate(5, 2, hebYear) == 6:
    if hebDay == 3 and hebMonth == 2:
      return ({1: "Yom HaAtzmaut"})
  elif getWeekdayOfHebrewDate(5, 2, hebYear) == 5:
    if hebDay == 4 and hebMonth == 2:
      return ({1: "Yom HaAtzmaut"})
  elif hebYear >= 5764 and getWeekdayOfHebrewDate(4, 2, hebYear) == 0:
    if hebDay == 6 and hebMonth == 2:
      return ({1: "Yom HaAtzmaut"})
  else:
    if hebDay == 5 and hebMonth == 2:
      return ({1: "Yom HaAtzmaut"})

  if hebDay == 18 and hebMonth == 2:
    return ({0: "Lag BOmer"})
  if hebDay == 28 and hebMonth == 2:
    return ({0: "Yom Yerushalayim"})

  # Holidays in Sivan
  if hebDay == 6 and hebMonth == 3 and is_sunday:
      return ({0: "Shavuot", 1: "Hag"})

  # Holidays in Av
  if hebDay == 9 and hebMonth == 5:
    return ({0: "Tisha BAv"})
  if hebDay == 15 and hebMonth == 5:
    return ({0: "Tu BAv"})

  # Holidays in Tishri
  if hebDay == 1 and hebMonth == 7 and is_sunday:
    return ({0: "Rosh Hashana", 1: "Hag"})
  if hebDay == 3 and hebMonth == 7 and is_friday:
    return ({1: "Shabbat Shuva"})
  if hebDay == 4 and hebMonth == 7 and is_friday:
    return ({1: "Shabbat Shuva"})
  if hebDay == 5 and hebMonth == 7 and is_friday:
    return ({1: "Shabbat Shuva"})
  if hebDay == 6 and hebMonth == 7 and is_friday:
    return ({1: "Shabbat Shuva"})
  if hebDay == 7 and hebMonth == 7 and is_friday:
    return ({1: "Shabbat Shuva"})
  if hebDay == 8 and hebMonth == 7 and is_friday:
    return ({1: "Shabbat Shuva"})
  if hebDay == 9 and hebMonth == 7 and is_friday:
    return ({1: "Shabbat Shuva"})
  #if hebDay == 10 and hebMonth == 7:
  #  return ({2: "Yom Kippur"})         #we want Shabbat Shuva to take precedence over Yom-Kippur
  if hebDay == 15 and hebMonth == 7 and is_sunday:
    return ({1: "Sukkot", 2: "Hag"})
  if hebDay == 16 and hebMonth == 7 and is_friday:
    return ({2: "Sukkot"})
  if hebDay == 17 and hebMonth == 7 and is_friday:
    return ({2: "Sukkot"})
  if hebDay == 18 and hebMonth == 7 and is_friday:
    return ({2: "Sukkot"})
  if hebDay == 19 and hebMonth == 7 and is_friday:
    return ({2: "Sukkot"})
  if hebDay == 20 and hebMonth == 7 and is_friday:
    return ({2: "Sukkot"})
  if hebDay == 21 and hebMonth == 7 and is_friday:
    return ({2: "Sukkot"})
  if hebDay == 22 and hebMonth == 7 and is_sunday:
    return ({0: "Simchat Torah", 1: "Hag"})		#take precendence over sukkot

  # Holidays in Kislev
  if hebDay == 25 and hebMonth == 9 and is_friday:	# we don't want music the shabbat before Hanukka
    return ({0: "Chanukka"})
  if hebDay == 26 and hebMonth == 9 and is_friday:
    return ({0: "Chanukka"})
  if hebDay == 27 and hebMonth == 9 and is_friday:
    return ({0: "Chanukka"})
  if hebDay == 28 and hebMonth == 9 and is_friday:
    return ({0: "Chanukka"})
  if hebDay == 29 and hebMonth == 9 and is_friday:
    return ({0: "Chanukka"})
  if date_utils.calendar_util.hebrew_month_days(hebYear, 9) == 30:
    if hebDay == 30 and hebMonth == 9 and is_friday:
      return ({0: "Chanukka"})
    if hebDay == 1 and hebMonth == 10 and is_friday:
      return ({0: "Chanukka"})
    if hebDay == 2 and hebMonth == 10 and is_friday:
      return ({0: "Chanukka"})
  if date_utils.calendar_util.hebrew_month_days(hebYear, 9) == 29:
    if hebDay == 1 and hebMonth == 10 and is_friday:
      return ({0: "Chanukka"})
    if hebDay == 2 and hebMonth == 10 and is_friday:
      return ({0: "Chanukka"})
    if hebDay == 3 and hebMonth == 10 and is_friday:
      return ({0: "Chanukka"})

  # Holidays in Shevat
  if hebDay == 15 and hebMonth == 11:
    return ({0: "Tu BShvat"})

  # Holidays in Adar (I)/Adar II
  if date_utils.calendar_util.hebrew_leap(hebYear):
    monthEsther = 13
  else:
    monthEsther = 12

  #if hebDay == 14 and hebMonth == monthEsther:
  if hebMonth == monthEsther and is_friday and hebDay < 14+7:	#play from begining of Adar, until the Shabbat after Purim
    return ({0: "Purim"})
  # if hebDay == 15 and hebMonth == monthEsther:
  #   listHolidays.append("Shushan Purim")

  return {}

def test_calculate_holiday():
  #A test program for the holiday calculation:

  year = 2019 #int(raw_input("Gregorian Year? "))
  nonleapgmonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  leapgmonths = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  for month in range(1,13):
    if date_utils.calendar_util.leap_gregorian(year):
      lastDay = leapgmonths[month-1]
    else:
      lastDay = nonleapgmonths[month-1]
    for day in range(1,lastDay+1):
      holidays = calculate_holiday(day, month, year, True)
      if len(holidays) > 0:
        print(str(day) + "/" + str(month) + "/" + str(year) + ": " + str(holidays))


def play_music_today(date):
  #returns true if this is erev_heg or Shabbat
  yesterday = date - datetime.timedelta(days=1)
  return (get_erev_hag(date.day, date.month, date.year) is not None or date.weekday() == 4) \
         and not (get_erev_hag(yesterday.day, yesterday.month, yesterday.year) or date.weekday() == 5)   # 4 == Friday, # 5 == Shabbat


def get_music_folders(date=datetime.date.today()):
  folders_dict = {}
  yesterday = date - datetime.timedelta(days=1)
  hag_name = get_erev_hag(date.day, date.month, date.year)
  if (hag_name):
    if (hag_name) in ('Yom Kippur', 'Rosh Hashana'):
      folders_dict = {0: hag_name, 1: 'Shabbat Shuva', 2: 'Hag', 3: 'Shabbat'}
    else:
      folders_dict = {0: hag_name, 2: 'Hag', 3: 'Shabbat'}
  elif date.weekday() == 4 and not get_erev_hag(yesterday.day, yesterday.month, yesterday.year):	# 4 == Friday
    folders_dict = {9: 'Shabbat'}		#lowest priority

    shabbat = date + datetime.timedelta(days=1)
    julian = date_utils.calendar_util.gregorian_to_jd(shabbat.year, shabbat.month, shabbat.day)
    hebYear, hebMonth, hebDay = date_utils.calendar_util.jd_to_hebrew(julian)
    str = getTorahSections(hebMonth, hebDay, hebYear, False)
    if str:
      folders_dict.update({8: str})	#second-lowest priority

    date_in_week = date				#Now look if there are any music-special-days this week
    for x in range(1, 7):
      date_in_week += datetime.timedelta(days=1)
      folders_dict.update(get_holiday(date_in_week.day, date_in_week.month, date_in_week.year))

  sorted_folders = []
  if len(folders_dict) > 0:
    for key in sorted(folders_dict):
      sorted_folders += [folders_dict[key]]

    print('{0}: {1}'.format(date, sorted_folders))
  return sorted_folders


def test_music_folders(year):
#A test program for the holiday calculation:
  date = datetime.date(year, 1, 1)
  for x in range(1, 366 if date_utils.calendar_util.leap_gregorian(year) else 365):
    if play_music_today(date):
      folders = get_music_folders(date)

    date += datetime.timedelta(days=1)
