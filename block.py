from ursina import *
from ursina.shaders import basic_lighting_shader
from ursina.shaders import triplanar_shader
from ursina.shaders import lit_with_shadows_shader
from ursinanetworking import *

BLOCKS_PARENT = Entity()

class Block(Button):

	def __init__(self, position = (0,0,0), is_player=False):
		super().__init__(
			parent = BLOCKS_PARENT,
			position = position,
			model = "cube",
			origin_y = .5,
			color = color.white,
			highlight_color=color.gray,
			scale = 1,
			shader = basic_lighting_shader
		)
		self.name = "unnamed_block"
		self.client = None
		self.breakable = True
		if (is_player):
			self.position = self.position + mouse.normal
		else:
			self.position = position

	