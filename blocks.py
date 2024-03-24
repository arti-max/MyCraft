from ursina import *
from block import *

class Grass(Block):
	def __init__(self, position=(0, 0, 0)):
		super().__init__(position)
		self.texture = "res/grass.png"
		self.breakable = True

class Stone(Block):
	def __init__(self, position=(0, 0, 0)):
		super().__init__(position)
		self.texture = "res/stone.png"
		self.breakable = True

class Planks(Block):
	def __init__(self, position=(0, 0, 0)):
		super().__init__(position)
		self.texture = "res/planks.png"
		self.breakable = True

class Adminium(Block):
	def __init__(self, position=(0, 0, 0)):
		super().__init__(position)
		self.texture = "res/adminium.png"
		self.breakable = False