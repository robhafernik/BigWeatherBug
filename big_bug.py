import sys
import time
from datetime import datetime
import pygame
import os
from settings import Settings
from weather import Weather

#
# This project implements a "Big"WeatherBug", a small, enclosed display
# that can be mounted on the wall to show the current temperature,
# weather conditions, and forecast.  It is written in Python using
# the Python game framework.
# 
# This uses the Raspberry Pi 3 single board computer, using the 
# 'PiTFT Plus 480x320 3.5" TFT+Touchscreen for Raspberry Pi' from 
# Adafruit for a display.  See https://www.adafruit.com/product/2441
# 
# The case is also from Adafruit and is specifically designed to fit this
# particular screen.  See https://www.adafruit.com/product/2779
# 
# This code uses weather data from OpenWeatherMap: http://openweathermap.org
#
# Adafruit is an excellent source for hobby electronics, check them out today!
#
# Written by Rob Hafernik, rob@hafernik.com
#
# My first go at this was the "Little Weather Bug", which is documented
# on GitHub at: https://github.com/robhafernik/LittleWeatherBug
# 
# This new version uses the display referenced above, along with the
# pygame library for python to draw the display.  Some complicaton is 
# added by having two color levels for everything: one for daytime and 
# one for nighttime (the day mode is just too bright at night).
#
# Released into the public domain, do with it as you will.  It is not,
# however, warranted to be correct in any way.
#

os.putenv('SDL_FBDEV', '/dev/fb1')

class BigBug:
	"""Newer, bigger, better weather bug"""

	def __init__(self):
		"""Initialize big weather bug"""

		self.settings = Settings()

		self.weather = Weather()

		pygame.init()

		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

		pygame.display.set_caption(self.settings.name)
		pygame.mouse.set_visible(False)

		self.big_font_sys = pygame.font.SysFont(None, 96)
		self.med_font_sys = pygame.font.SysFont(None, 48)
		self.sm_font_sys = pygame.font.SysFont(None, 36)

	def run_bug(self):
		"""Main loop for weather bug"""

		while True:

			# only event to trap is quit
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			self.screen.fill(self.settings.background_day)

			# get weather
			self.weather.fetch_weather()

			# draw it
			self.draw_bug()
			pygame.display.flip()

			# sleep several seconds
			time.sleep(self.settings.sleep_time)

	def draw_bug(self):
		"""Draw to the Screen"""

		big_font = self.big_font_sys
		med_font = self.med_font_sys
		sm_font = self.sm_font_sys

		# date and time, color index to dim at night
		now = datetime.now()
		night_or_day = 1  # night
		if((now.hour > 6) and (now.hour < 18)):
			night_or_day = 0  # day

		tstr = now.strftime("%H:%M")
		dstr = now.strftime("%a, %b %d")
		self.draw_text_ra(tstr, big_font, 460, 320, self.settings.time_color[night_or_day])
		self.draw_text_la(dstr, med_font, 20, 314, self.settings.date_color[night_or_day])

		# current conditions
		self.draw_text_la(self.weather.curr_temp, big_font, self.weather.curr_temp_left, self.weather.curr_temp_bottom, self.weather.curr_color[night_or_day])
		self.draw_text_la(self.weather.curr_conditions, med_font, self.weather.curr_cond_left, self.weather.curr_cond_bottom, self.weather.curr_conditions_color[night_or_day]) 

		# forecast
		bottom = self.weather.forecasts_start
		height = self.weather.forecasts_height
		time_right = self.weather.forecasts_time_right
		fcast_left = self.weather.forecasts_fcast_left
		time_color = self.weather.forecasts_time_color[night_or_day]
		fcast_color = self.weather.forecasts_fcast_color[night_or_day]

		for fc in self.weather.forecasts:
			self.draw_text_ra(fc["time"], sm_font, time_right, bottom, time_color)
			self.draw_text_la(fc["fcast"], sm_font, fcast_left, bottom, fcast_color)
			bottom += height

		# some separators
		pygame.draw.line(self.screen,(0, 200, 200),(8,70),(472,70))
		pygame.draw.line(self.screen,(0, 200, 200),(8,246),(472,246))


	def draw_text_la (self, text, font, left, bottom, color):
		"""Draw text, left-aligned"""
		img = font.render(text, True, color, self.settings.background_day)
		rect = img.get_rect()
		rect.bottom = bottom
		rect.left = left
		self.screen.blit(img, rect)

	def draw_text_ra(self, text, font, right, bottom, color):
		"""Draw text, right-aligned"""
		img = font.render(text, True, color, self.settings.background_day)
		rect = img.get_rect()
		rect.bottom = bottom
		rect.right = right
		self.screen.blit(img, rect)

# This gets us started:
if __name__ == '__main__':
	big_weather_bug = BigBug()
	big_weather_bug.run_bug()

