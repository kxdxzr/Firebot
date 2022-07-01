class Tree:

	#
	# TODO
	#

	def __init__(self, height):
		#
		# TODO
		#
		self.height=int(height)
		self.intensity=0
		self.Burnt_down=False
		self.spread=True
	
	def show_height(self):
		if self.Burnt_down==True:
			return "x"
		if self.height==0:
			return " "
		return self.height
	
	def show_intensity(self):
		if self.Burnt_down==True:
			return "x"
		if self.height==0:
			return " "
		elif self.intensity==0:
			return "."
		if self.intensity>9:
			return 9
		return self.intensity
