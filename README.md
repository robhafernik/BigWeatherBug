* BigWeatherBug


From the big_bug.py file in this project:

*
* This project implements a "Big"WeatherBug", a small, enclosed display
* that can be mounted on the wall to show the current temperature,
* weather conditions, and forecast.  It is written in Python using
* the Python game framework.
* 
* This uses the Raspberry Pi 3 single board computer, using the 
* 'PiTFT Plus 480x320 3.5" TFT+Touchscreen for Raspberry Pi' from 
* Adafruit for a display.  See https://www.adafruit.com/product/2441
* 
* The case is also from Adafruit and is specifically designed to fit this
* particular screen.  See https://www.adafruit.com/product/2779
* 
* This code uses weather data from OpenWeatherMap: http://openweathermap.org
*
* Adafruit is an excellent source for hobby electronics, check them out today!
*
* Written by Rob Hafernik, rob@hafernik.com
*
* My first go at this was the "Little Weather Bug", which is documented
* on GitHub at: https://github.com/robhafernik/LittleWeatherBug
* 
* This new version uses the display referenced above, along with the
* pygame library for python to draw the display.  Some complicaton is 
* added by having two color levels for everything: one for daytime and 
* one for nighttime (the day mode is just too bright at night).
*
* Released into the public domain, do with it as you will.  It is not,
* however, warranted to be correct in any way.
*
