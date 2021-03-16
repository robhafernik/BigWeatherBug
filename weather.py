import time
import urllib.request
import json

#
# Get a free APP ID from openweather and use it to call their APIs for current weather and forecase weather
#
# OpenWeather APIs:
# Current observations: http://api.openweathermap.org/data/2.5/weather?id=4671654&units=imperial&APPID=<Your APP ID Here>
# Forecast: http://api.openweathermap.org/data/2.5/forecast?id=4671654&units=imperial&APPID=<Your APP ID Here>\
#
class Weather:
	"""A class the holds weather observations and forecast"""

	def __init__(self):
		"""initialize the weather object""" 

		self.name = "Weather for Austin, TX"
		
		self.api_key = "<Yur API ID from OpenWeather Here>"
		self.city_id = "4671654"  # City code for Austin, TX
		self.curr_temp = "..."
		self.curr_conditions = "looking up weather..."
		self.curr_color = (100, 100, 100)
		self.curr_conditions_color = [(200, 200, 200), (140, 140, 140)]
		self.curr_temp_left = 4
		self.curr_temp_bottom = 70
		self.curr_cond_left = 116
		self.curr_cond_bottom = 64
		self.curr_last_update = 0
		self.curr_freq = 600

		forecast0 = { 'time': '--', 'fcast': '--' }
		forecast1 = { 'time': '--', 'fcast': '--' }
		forecast2 = { 'time': '--', 'fcast': '--' }
		forecast3 = { 'time': '--', 'fcast': '--' }
		self.forecasts = [forecast0, forecast1, forecast2, forecast3]

		self.forecasts_last_update = 0
		self.forecasts_freq = 3600

		self.cold    = [(100, 100, 200), (80, 80, 160)]
		self.mild    = [(100, 200, 100), (80, 160, 80)]
		self.warm    = [(200, 200, 100), (120, 120, 60)]
		self.hot     = [(240, 100, 100), (140, 60, 60)]
		self.scortch = [(250, 150, 30), (180, 100, 20)]

		self.forecasts_start = 112
		self.forecasts_height = 42
		self.forecasts_time_right = 166
		self.forecasts_fcast_left = 172
		self.forecasts_time_color = [(90, 120, 90), (80, 100, 80)]
		self.forecasts_fcast_color = [(130, 170, 130), (100, 130, 100)]

	def fetch_weather(self):
		"""Fetch the weather, if enough time has passed since last time"""

		now = time.time()

		# current conditions
		since_current = now - self.curr_last_update
		if(since_current > self.curr_freq):

			# go fetch current conditions, if it works don't do it again for self.curr_freq seconds
			if(self.fetch_current() == True):
				self.curr_last_update = now

		# forecast
		since_forecast = now - self.forecasts_last_update
		if(since_forecast > self.forecasts_freq):

			# go fetch forecast, if it works, don't do it again for self.forecasts_freq seconds
			if(self.fetch_forecast() == True):
				self.forecasts_last_update = now

	def fetch_current(self):
		"""HTTP Get the current conditiions"""

		success = False
		try:
			url = "http://api.openweathermap.org/data/2.5/weather?id=" + self.city_id + "&units=imperial&APPID=" + self.api_key
			open_url = urllib.request.urlopen(url)

			json_data = None
			if((open_url != None) and (open_url.getcode()==200)):
				# parse out the JSON
				data = open_url.read()
				json_data = json.loads(data)

			if(json_data != None):
				# temperature
				main = json_data["main"]
				temp = main["temp"]
				self.curr_temp = str(round(temp))

				# temp color
				if(temp < 50):
					self.curr_color	= self.cold
				elif (temp < 70):
					self.curr_color	= self.mild
				elif (temp < 95):
					self.curr_color	= self.warm
				elif (temp < 100):
					self.curr_color	= self.hot
				else:
					self.curr_color	= self.scortch

				# humidity
				humid = str(round(main["humidity"]))

				# description
				weath = json_data["weather"][0]
				cond = weath["description"]
				cond = cond.title()
				self.curr_conditions = f"{humid}%  {cond}"
				success = True
			else:
				self.curr_contitions = "-JSON Error-"
		except Exception as e:
			self.curr_conditions = "-HTTP Error-"
			print("Current Conditions Exception: ", str(e))

		return success

	def fetch_forecast(self): 
		"""HTTP Get the forecast"""

		success = False
		try:
			url = "http://api.openweathermap.org/data/2.5/forecast?id=" + self.city_id + "&units=imperial&APPID=" + self.api_key
			open_url = urllib.request.urlopen(url)

			json_data = None
			if((open_url != None) and (open_url.getcode()==200)):
				data = open_url.read()
				json_data = json.loads(data)

			if(json_data != None):
				fclist = json_data["list"]

				index = 0
				item_count = 0
				for item in fclist:
					if((item_count == 0) or (item_count == 2) or (item_count == 4) or (item_count == 6)):
						dt_txt = item["dt_txt"]
						dt_fix = self.fix_time(dt_txt)

						main = item["main"]
						temp = str(round(main["temp"]))
						humidity = str(round(main["humidity"]))

						weather = item["weather"][0]
						desc = weather["description"]
						desc = desc.title()

						fc = self.forecasts[index]

						fc["time"] = dt_fix
						fc["fcast"] = f"{temp}, {humidity}%, {desc}"
						index = index + 1
					item_count = item_count + 1
				success = True
			else: 
				for fc in self.forecasts:
					fc["time"] = "--"
					fc["fcast"] = "-JSON Error-"

		except Exception as e:
			for fc in self.forecasts:
					fc["time"] = "--"
					fc["fcast"] = "-HTTP Error-"
			print("Forecast Exception: ", str(e))

		return success


	def fix_time(self, tstr):
		"""Turn something like 2020-06-29 18:00:00 UTC into a human-readable string"""

		rstr = "?"
		hstr = tstr[11:13]

		if((hstr == "20") or (hstr == "21") or (hstr == "22") or (hstr == "23") or (hstr == "00")):  # 00:00 UTC is about 6PM CENTRAL
			rstr = "Afternoon:"
		elif ((hstr == "01") or (hstr == "02") or (hstr == "03") or (hstr == "04")):
			rstr = "Evening:"
		elif ((hstr == "05") or (hstr == "06") or (hstr == "07")):
			rstr = "Late Night:"
		elif ((hstr == "08") or (hstr == "09") or (hstr == "10") or (hstr == "11")):
			rstr = "Early Morning:"
		elif ((hstr == "12") or (hstr == "13") or (hstr == "14") or (hstr == "15") or (hstr == "16")):
			rstr = "Morning:"
		elif ((hstr == "17")or (hstr == "18") or (hstr == "19")):
			rstr = "Mid-Day:"
		else:
			rstr = hstr

		return rstr
 
