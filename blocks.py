from ursina import *
from block import *

class Grass(Block):
	def __init__(self, position=(0, 0, 0)):
		super().__init__(position)
		self.texture = "res/grass.png"
		self.breakable = True
		self.id = 1

class Stone(Block):
	def __init__(self, position=(0, 0, 0)):
		super().__init__(position)
		self.texture = "res/stone.png"
		self.breakable = True
		self.id = 2

class Planks(Block):
	def __init__(self, position=(0, 0, 0)):
		super().__init__(position)
		self.texture = "res/planks.png"
		self.breakable = True
		self.id = 3

class Adminium(Block):
	def __init__(self, position=(0, 0, 0)):
		super().__init__(position)
		self.texture = "res/adminium.png"
		self.breakable = False
		self.id = 0