# pythonista-scripts
Useful scripts to be run in Pythonista for iOS.  Kudos to [@cclauss](https://github.com/cclauss) for line by line code cleanup and helpful comments on improving these scripts.

- **BibleVerses.py** - This Pythonista script will retrieve any bible verse or verses and copy them to the clipboard or 1Writer, Editorial, or Drafts via a url. The script uses the getBible.net api as the query source for scripture.  More info is available [here](https://getbible.net/api) and in the script comments.  The script can be initialized stand alone from Pythonista or from a url action in 1Writer, Editorial, or Drafts.  If run stand alone, the script will copy the verse(s) returned from the query to the clipboard and print them to the console. You can then copy the verses to any application you wish using the clipboard.  If the script is called from one of the 3 text editors mentioned above via a url, the scripture will be appended to the calling editor's open doc.  Inspiration for this script came from @pfcbenjamin and his script [BibleDraft.py](https://gist.github.com/pfcbenjamin/423b27d4a56635220be9). More info is available [here](https://sweetnessoffreedom.wordpress.com/projects/bibledraft).

- **Search IMDB.py** - A script that I find useful to quickly look up info on a movie title or a TV series.  The results of the query are displayed on the console screen and a Markdown version is copied to the clipboard for pasting to a text editor. The script also allows for the query results to be written to a choice of popular apps including 1Writer, DayOne, Drafts, and Editorial using their respective URL schemes.

- **PhotosToDropbox.py** - A script that lets you select multiple photos from the iPhone camera roll, resize & geo-tag them, and upload them to Dropbox where they are renamed and organized based on the date and time they were taken.  The cool part is that the script will preserve the metadata of the original photo if desired, using the [Pexif module](https://github.com/bennoleslie/pexif) to read the metadata from the original and write it back to the resized copy.  The Pexif module can be imported into Pythonista by simply copying pexif.py into the Pythonista script directory.  The script requires [DropboxLogin.py](https://gist.github.com/omz/4034526) to allow Pythonista login access to your Dropbox account. 

- **WeatherAnywhere.py** - This script was inspired by @cclauss' script '[weather_where_you_are.py](https://github.com/cclauss/weather_where_you_are)' and uses the [weather api](http://www.wunderground.com/weather/api) from www.wunderground.com.  The script displays all it's information on the console screen, ideally suited for an iPhone in portrait orientation. In order to use the script you will need to aquire an api key from the wunderground website. The key is free if your usage is 500 or less server hits per day and provides a wealth of weather information. Lots of weather info is provided in text, including forecast, humidity, pressure, temperature, precipitation amounts, wind speed, wind chill, & percent of precipitation. The info is in imperial units, but can easily be changed to metric via a flag in the script. The script makes use of a txt file, 'cities.txt', to be located in the same folder as the script, and 38 gif files that display weather types, located in the '/icons' subfolder of the script's folder. The script will download the icons if it doesn't find them.  The txt file can contain popular local, regional, national and international cities of your choosing, including their state, if national, or country, if international, and their zip links.  The file is easily editable with the Pythonista editor. The zip link is automatically added to the cities list when you choose to add a new city. I've included a sample cities.txt file in this repository. 

- **cities.txt** - A sample txt file for 'WeatherAnywhere.py'.  Put it in the same folder as the script.

- **WeatherAnywhereScene.py** - Inspiration behind this was @cclauss's script, [WeatherAnywhereView.py](https://github.com/coomlata1/pythonista-scripts/blob/master/wa_open_weather_map/WeatherAnywhereView.py) in this repository. I wanted to be able to add weather icons and have them scroll with the text, so a scene seemed to be the best answer. This script gives a much better representation of the weather info than the console version does. It displays the current weather, weather for the next 24 hrs, weather for the next 7 days, and buttons on the title bar for viewing the weather on the web and weather alerts for the region.  The script uses the functions in 'WeatherAnywhere.py' to retrieve the necessary weather info displayed.  The script allows scrolling the scene by inertia.  A basic scrolling example was created by Dalorbi on the [pythonista forums](http://omz-forums.appspot.com/pythonista/post/4998190881308672). Ability for scrolling the scene with inertia was added by [hroe](https://gist.github.com/henryroe/6724117). This script needs to be placed in the same folder as WeatherAnywhere.py, to make use of some of it's functions. The script also uses the weather icons stored in a subfolder '/icons' off the script folder.

- **SendGpsData.py** -  A Pythonista script for texting your GPS location & current weather using clipboard, email, or SMS messaging. Requires [Launch Center Pro](https://itunes.apple.com/us/app/launch-center-pro/id532016360?mt=8) to provide ability to email and SMS msg the text, and an api key from [here](http://www.wunderground.com/weather/api) to get weather data. The script can be run stand alone from Pythonista or be called from 1Writer, Editorial, or Drafts via a URL, in which case the text will be appended to the caller's open doc for use in journaling, logs, etc. Github contributors to this script are noted in script's comments.

- **ListToFantastical2.py** - This script parses BOTH reminders and events from comma seperated text passed from URL's in LCP, 1Writer, or Drafts and posts them in Fantastical2 and returns you to the caller app. Thanks to Fantastical's natural language parsing, your 'tasks' can be reminders or events.  The reminders must start with a 'Task', 'Todo', 'Reminder', or 'Remind me' pre-text followed by the
todo itself.  Events don't need the pre-text. For more on this see [here](http://www.geekswithjuniors.com/note/5-awesome-things-from-fantastical-2-that-can-improve-your-wo.html)
and [here](http://plobo.net/recursive-actions-with-launchcenterpro-and-pythonista) for 2 well documented intros to the proper syntax. Inspiration came from [this](https://gist.github.com/pslobo/25af95742e1480210e2e) script.  Thanks goes to @pslobo for his Github contribution. 

