from ursina import *


id_1 = "res/grass.png"
id_2 = "res/stone.png"
id_3 = "res/planks.png"
button = "res/button.png"

class SB(Entity):
	def __init__(self, texture=id_1):
		super().__init__(
			parent=camera.ui,
			model='cube',
			texture=texture,
			position=Vec2(0.7, 0.4),
			scale=(0.1, 0.1, 0.1)
			)
