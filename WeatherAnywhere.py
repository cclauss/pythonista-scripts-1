#coding: utf-8

# Name: WeatherAnywhere.py
# Author: John Coomler
# v1.0: 02/07/2015 to 02/15/2015-Created
# v1.1: 02/19/2015-Tightened up code and
# made function calls to retrieve weather
# data for printing from main(). Many
# thanks to @cclauss for his continued
# expertise, input, & support in sorting
# out and improving the code.
# v1.2: 02/20/2015-More code cleanup,
# improved string formatting techniques,
# and much improved error handling.
# v1.3: 02/21/2015-Added function to
# download weather icons if any or all
# are missing. More code cleanup.
'''
This script provides current and multi day
weather forecasts for any city you name,
or coordinates you are currently located
in, using the api available from
www.openweathermap.org. The inspiration
for this script came from https://
github.com/cclauss/weather_where_you_are/
weather_where_you_are.py. The conversion
functions used here were found at http://
jim-easterbrook.github.io/pywws/doc/en/
html/_modules/pywws/conversions.html
'''
import console
import csv
import datetime
import location
from PIL import Image
import requests
import sys

# Global variables
icons=[]
missing_icons=[]
# Number of days in advaced forecast
day_count=7
# Change to 'metric' if desired
imperial_or_metric='imperial'

def get_current_lat_lon():
  # Retrieve lat & lon from current locale
  location.start_updates()
  # Delay sometimes improves accuracy
  #time.sleep(1)
  address_dict = location.get_location()
  location.stop_updates()
  return address_dict['latitude'],address_dict['longitude']

def city_ids(filename='cities.csv'):
  try:
    with open(filename) as in_file:
      # Read each line and store in list
      ids = [row for row in csv.reader(in_file)]
  except IOError as e:
    sys.exit('IOError in city_ids(): {}'.format(e))
  if not ids:
    sys.exit('No cities found in: {}'.format(filename))
  for i, id in enumerate(ids):
    # Align numbers neatly in printed list of cities & countries
    print('{:>7}. {}, {}'.format(i, id[0], id[1]))
  while True:
    try:
      ans = int(raw_input('\nEnter number of desired city: '))
      # Retrieve data from proper row,
      city, country, id = ids[ans]
      return city, country, id
    except (IndexError, ValueError):
      print('Please enter a vaild number.')

def get_weather_dicts(lat,lon,city,id):
  url_fmt = 'http://api.openweathermap.org/data/2.5/{}?{}'
  if city: # From entered city
    fmt = 'q={}&type=accurate&units={}'
    query = fmt.format(city, imperial_or_metric)
  elif id: # From list
    fmt = 'id={}&type=accurate&units={}'
    query = fmt.format(id, imperial_or_metric)
  else: # From where you are now
    fmt = 'lat={}&lon={}&type=accurate&units={}'
    query = fmt.format(lat, lon, imperial_or_metric)

  w_url = url_fmt.format('weather', query)

  query += '&cnt={}'.format(day_count)
  f_url = url_fmt.format('forecast/daily', query)
  try:
    weather = requests.get(w_url).json()
    forecast = requests.get(f_url).json()
    #import pprint;pprint.pprint(weather)
    #import pprint;pprint.pprint(forecast)
    #See: http://bugs.openweathermap.org/projects/api/wiki
    #sys.exit()
  except requests.ConnectionError:
    print('=' * 20) # console.clear()
    sys.exit('Weather servers are busy. Try again in a few minutes...')
  return weather, forecast

def precip_inch(mm):
    # Convert rain or snowfall from mm to in
  return '{:.2f}'.format(mm/25.4)

def wind_dir(deg):
  # Convert degrees to wind direction
  assert 0 <= deg <= 360, 'wind_dir({}): deg is out of bounds!'.format(deg)
  if   deg < 11.25:   return 'N'
  elif deg < 33.75:   return 'NNE'
  elif deg < 56.25:   return 'NE'
  elif deg < 78.75:   return 'ENE'
  elif deg < 101.25:  return 'E'
  elif deg < 123.75:  return 'ESE'
  elif deg < 146.25:  return 'SE'
  elif deg < 168.75:  return 'SSE'
  elif deg < 191.25:  return 'S'
  elif deg < 213.75:  return 'SSW'
  elif deg < 236.25:  return 'SW'
  elif deg < 258.75:  return 'WSW'
  elif deg < 281.25:  return 'W'
  elif deg < 303.75:  return 'WNW'
  elif deg < 326.25:  return 'NW'
  elif deg < 348.75:  return 'NNW'
  return 'N'

def wind_mph(mps):
  # Convert wind from meters/sec to mph
  return '{:.0f}'.format(mps*3.6/1.609344)

def wind_chill(temp,wind):
  '''
  Compute wind chill using formula from
  http://en.wikipedia.org/wiki/wind_chill
  '''
  temp=float(temp)
  wind=float(wind)
  if wind<=3 or temp>50:
    return temp
  return '{:.0f}'.format(min(35.74+(temp*0.6215)+(((0.3965*temp)-35.75)*(wind**0.16)),temp))

def pressure_inhg(hPa):
  # Convert pressure from hectopascals/millibar to inches of mecury
  return '{:.2f}'.format(hPa/33.86389)

def download_weather_icons():
  # Downloads any missing weather icons
  # from www.openweathermap.org
  import os
  fmt = 'Downloading {} from {} ...'
  for i in (1,2,3,4,9,10,11,13,50):
    filenames = ('{:02}d.png'.format(i), '{:02}n.png'.format(i))
    for filename in filenames:
      if os.path.exists(filename):
        continue
      url = 'http://openweathermap.org/img/w/' + filename
      with open(filename, 'w') as out_file:
        try:
          print(fmt.format(filename, url))
          out_file.write(requests.get(url).content)
        except requests.ConnectionError as e:
          print('ConnectionError on {}: {}'.format(i ,e))
      print('Done.')

def get_current_weather(w):
  # Current weather conditions
  #for item in ('temp_min', 'temp_max'):
    #if item not in w['main']:
      #w['main'][item] = None # create values if they are not present

  #if 'weather' not in w:
    #w['weather']=[{'description' : 'not available'}]

  # Round current temp to whole number
  w['main']['temp']='{:.0f}'.format(w['main']['temp'])

  # Pressure & convert to inches
  w['main']['pressure']=pressure_inhg(w['main']['pressure'])

  # Capitalize weather description
  w['weather'][0]['description']=w['weather'][0]['description'].title()

  # Convert wind degrees to wind direction
  w['wind']['deg']=wind_dir(w['wind']['deg'])

  # Convert wind speed to mph
  w['wind']['speed']=wind_mph(w['wind']['speed'])

  # Get wind chill factor using temp & wind speed
  chill=wind_chill(w['main']['temp'],w['wind']['speed'])

  try:
    # Get wind gusts and covert to mph, although they aren't always listed'
    w['wind']['gust']=float(wind_mph(w['wind']['gust']))+float(w['wind']['speed'])
    gusts='Gusts to {}'.format(w['wind']['gust'])
  except:
    gusts=''
  # Convert timestamp to date of weather
  w['dt']=datetime.datetime.fromtimestamp(int(w['dt'])).strftime('%A\n  %m-%d-%Y @ %I:%M %p:')

  # Do same for sunrise,sunset timestamps
  for item in ('sunrise', 'sunset'):
    w['sys'][item]=datetime.datetime.fromtimestamp(int(w['sys'][item])).strftime('%I:%M %p')

  # Find icon name in data
  ico=w['weather'][0]['icon']+'.png'
  #Open, resize and show weather icon
  try:
    i=Image.open(ico).resize((25,25),Image.ANTIALIAS)
    i.show()
  except:
    # Maybe no icons or some missing
    missing_icons.append(ico)

  # Return the reformated data
  weather=('''Today's Weather in {name}:\n
Current Conditions for {dt}
  {weather[0][description]}
  Clouds: {clouds[all]}%
  Temperature: {main[temp]}° F
  Humidity: {main[humidity]}%
  Barometric Pressure: {main[pressure]} in
  Wind: {wind[deg]} @ {wind[speed]} mph {}
  Feels Like: {}° F
  Sunrise: {sys[sunrise]}
  Sunset: {sys[sunset]}\n'''.format(gusts,chill,**w))
  return weather

def get_forecast(f):
  # Extended forecast
  sp=' ' * 4

  forecast= 'Extended '+str(day_count)+' Day Forecast for '+str(f['city']['name'])+':\n'

  # Loop thru each day
  for i in xrange(day_count):
    # Get icon name and store in list
    ico=f['list'][i]['weather'][0]['icon']+'.png'
    icons.append(ico)

    # Timestamp of forecast day formatted to m-d-y
    forecast+='\nForecast for '+datetime.datetime.fromtimestamp(int(f['list'][i]['dt'])).strftime('%A %m-%d-%Y')

    # Capitalize weather description
    forecast+='\n'+sp+f['list'][i]['weather'][0]['description'].title()

    # Get type of preciptation
    precip_type=f['list'][i]['weather'][0]['main']
    # Get measured amts of precip
    if precip_type in ('Rain', 'Snow'):
      try:
        # Convert precip amt to inches
        forecast+='\n'+sp+'Expected '+precip_type+' Vol for 3 hrs: '+precip_inch(f['list'][i][precip_type.lower()])+' in'
      except:
        # Sometimes precip amts aren't listed
        pass
    elif precip_type=='Clouds':
      forecast+='\n'+sp+'No Rain Expected'

    # Cloudiness percentage
    forecast+='\n'+sp+'Clouds: '+str(f['list'][i]['clouds'])+'%'

    # High temp rounded to whole number
    forecast+='\n'+sp+'High: {:.0f}'.format(f['list'][i]['temp']['max'])+'° F'

    # Low temp rounded the same
    forecast+='\n'+sp+'Low: {:.0f}'.format(f['list'][i]['temp']['min'])+'° F'

    # Humidity
    forecast+='\n'+sp+'Humidity: '+str(f['list'][i]['humidity'])+'%'

    # Pressure formatted to inches
    forecast+='\n'+sp+'Barometric Pressure: '+str(pressure_inhg(f['list'][i]['pressure']))+' in'

    # Wind direction and speed
    forecast+='\n'+sp+'Wind: '+str(wind_dir(f['list'][i]['deg']))+' @ '+str(wind_mph(f['list'][i]['speed']))+' mph'
    # Blank line between forecasted days
    forecast+='\n'

  return forecast

def main():
  console.clear()
  city = country = id = ''
  lat = lon = 0
  # Pick a weather source
  try:
    ans=console.alert('Choose Your Weather Source:','','From Your Current Location','From Entering a City Name','From A Pick List of Cities')
    if ans==1:
      # Weather where you are
      print 'Gathering weather data from where you are...'
      # Get lat & lon of where you are
      lat,lon=get_current_lat_lon()
    elif ans==2:
      # Enter a city & country
      msg='Enter a city and country in format "'"New York, US"'": '
      ans=console.input_alert(msg).title()
      if ans:
        print('='*20)
        print 'Gathering weather data for '+ans
        city=ans.replace(' ','+')
    elif ans==3:
      # Pick from list
      theCity,country,id=city_ids()
      print('='*20)
      if id:
        print 'Gathering weather data for '+theCity+', '+country
  except Exception as e:
    sys.exit('Error: {}'.format(e))

  # Call api from www.openweathermap.org
  w,f=get_weather_dicts(lat,lon,city,id)

  print('='*20)
  # Print current conditions to console
  print(get_current_weather(w))
  '''
  Printing the extended forecast to the
  console involves a bit more code because
  we are inserting a weather icon at each
  blank line.
  '''
  extended_f=get_forecast(f).split('\n')
  count=0
  for line in extended_f:
    '''
    Look for blank lines and don't exceed
    the number of forecasted days -1 for
    zero base in array holding icon names
    '''
    if not line and count<=(day_count-1):
      ico=icons[count]
      try:
        # Open, resize and show weather icon
        img=Image.open(ico).resize((25,25),Image.ANTIALIAS)

        img.show()
      except:
        missing_icons.append(ico)
      count += 1
    print line

  print 'Weather information provided by openweathermap.org'

  if missing_icons:
    ans=console.alert('Weather Icon(s) Missing:','','Download Them Now')
    if ans==1:
      download_weather_icons()

if __name__ == '__main__':
  main()
