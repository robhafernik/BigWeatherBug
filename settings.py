class Settings:
	"""A class the holds settings for the big_bug program"""

	def __init__(self):
		"""initialize the big weather bug's settings"""

		self.name = "Big Weather Bug"
		self.screen_width = 480
		self.screen_height = 320
		self.background_day = (0, 0, 0)
		self.background_night = (0, 0, 0)

		self.time_color = [(240, 240, 240), (140, 140, 140)]
		self.date_color = [(160, 160, 160), (120, 120, 120)]

		self.sleep_time = 10