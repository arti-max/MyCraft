from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class Player(FirstPersonController):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.mouse_sensitivity = (155,155)
		self.position=(5,15,5)
		self.camera_pivot.y = 1.5
		self.jump_height = 1.2

class PlayerRepresentation(Entity):
    def __init__(self, position = (5,15,5)):
        super().__init__(
            parent = scene,
            position = position,
            model = "cube",
            texture = "white_cube",
            origin_y = .5,
            color = color.white,
            highlight_color = color.white,
            scale = (0.5, 1.4, 0.5)
        )
        print("New Player Spawned")