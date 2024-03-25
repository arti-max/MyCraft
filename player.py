from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class Player(FirstPersonController):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.mouse_sensitivity = (155,155)
		self.position=(0,15,0)
		self.camera_pivot.y = 1.5
		self.jump_height = 1.2