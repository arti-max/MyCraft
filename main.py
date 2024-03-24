from ursina import *
from ursinanetworking import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import noise_fog_shader
from ursina.shaders import basic_lighting_shader
import configparser
from random import *
from tkinter import *
from pickle import *
import os
import json
import dill
#------GAME CLASSES---------
from blocks import *
from player import *
from UI import *
from level.levelGenerate import *
from level.levelSave import *
from level.levelLoad import *

def find_index(main_arr, sub_arr):
    try:
        index = main_arr.index(sub_arr)
        return index
    except ValueError:
        return -1

BLOCKS = [
	"grass",
	"stone",
	"planks"
]

#def Quit():
	#sys.exit()

#def Resume(self):
	#player.enabled = True


#-------CONFIG-----------
config = configparser.ConfigParser()

config.add_section('settings')
config.set('settings', 'render-distance', '45')
if os.path.exists("config.cfg"):
	print("true")
else:
	with open('config.cfg', 'w') as cfg:
		config.write(cfg)
config.read('config.cfg')
cfg_value1 = config.get('settings', 'render-distance')
cfg_value1 = int(cfg_value1)

Game = Ursina(title="MyCraft", icon="res/stone.ico", development_mode=False, borderless = False)
window.exit_button.enabled = False
window.cog_button.enabled = False
window.fullscreen = False
window.position=Vec2(100, 100)

camera.clip_plane_far=cfg_value1

i = 0
bid = f"block_{i}"
block_id = 1

sky_texture = load_texture("res/sky_blue.png")



if (os.path.exists("level.dat")):
	LEVEL = levelLoad("level.dat")
	for i in range(len(LEVEL)):
		bid = f"block_{i}"
		if (LEVEL[i][1] == 0):
			block = Adminium((LEVEL[i][0]))
		if (LEVEL[i][1] == 1):
			block = Grass((LEVEL[i][0]))
		if (LEVEL[i][1] == 2):
			block = Stone((LEVEL[i][0]))
		if (LEVEL[i][1] == 3):
			block = Planks((LEVEL[i][0]))
		new_block = block
		new_block.name = bid
		LEVELBLOCKS[bid] = new_block
		POSgenerate(LEVEL[i][0])
		i+=1
else:
	for x in range(15):
		for z in range(15):
			for y in range(4):
				bid = f"block_{i}"
				if (y == 0):
					block = Adminium((x, y, z))
					block_id = 0
				else:
					if (block_id == 1):
						block = Grass((x, y, z))
				new_block = block
				new_block.name = bid
				LEVELBLOCKS[bid] = new_block
				levelGenerate(block.position, block_id)
				block_id = 1
				i+=1

"""if os.path.exists("save.dat"):
	with open("save.dat", "rb") as save:
		world = dill.load(save)
		#worldBlocks = pickle.load(save)
	print(world)

	for i in range(len(world)):
		bid = f"block_{i}"
		if world[i][3] == 1:
			blockS = Grass()
		elif world[i][3] == 2:
			blockS = Stone()
		elif world[i][3] == 3:
			blockS = Planks()
		new_block = blockS
		new_block.name = bid
		new_block.id = world[i][3]
		new_block.position = (world[i][0],world[i][1], world[i][2])
		worldBlocks[bid] = new_block
		print(world[i])
		i += 1

else:
	if len(world) == 0:
		for z in range(20):
			for x in range(20):
				for y in range(-5, 0):
					bid = f"block_{i}"
					if y == -1:
						block_id = 1
						block = Grass()
						world.append([x, y, z, block_id])
					else:
						block_id = 2
						block = Stone()
						world.append([x, y, z, block_id])
					new_block = block
					new_block.name = bid
					new_block.id = block_id
					new_block.position = (x, y, z)
					worldBlocks[bid] = new_block
					index = find_index(world, [x, y, z, block_id])
					if index < i:
						destroy(worldBlocks[bid])
						del worldBlocks[bid]
						print("dublicate")
					else:
						i += 1
					block_id = 1
with open("save.dat", "wb") as save:
	dill.dump(world, save)"""



#print (worldBlocks)
print("massive len: ", len(LEVEL))
print("dict len: ", len(LEVELBLOCKS))
player = Player()

def input(key):
		global block_id
		global bid
		global i

		if key == "right mouse down":
			A = raycast(player.position + (0, 1.5, 0), camera.forward, distance = 6, traverse_target = scene, debug=True)
			E = A.entity
			if E:
				print("camera: ", camera.forward)
				pos = E.position + mouse.normal
				pos = tuple(pos)
				bid = f"block_{i}"
				posY = int(E.position.y)
				print("Old pos: ", E.position.x, posY, E.position.z)
				index = find_index(LEVELPOS, [int(E.position.x), posY, int(E.position.z)])
				if (index != -1):
					print(index)
				if block_id == 1: block = Grass(pos)
				elif block_id == 2: block = Stone(pos)
				elif block_id == 3: block = Planks(pos)
				new_block = block
				new_block.name = bid
				LEVELBLOCKS[bid] = new_block
				print("New pos: ", E.position.x, posY, E.position.z)
				LEVEL.append([pos, block_id])
				levelSave(LEVEL, "level.dat")
				i += 1
				#print (Blocks)
				#print (bid)
		if key == "left mouse down":
			A = raycast(player.position + (0, 1.5, 0), camera.forward, distance = 6, traverse_target = scene)
			E = A.entity
			if E and E.breakable:
				block_name = E.name
				#for i in range(randrange(2, 4)):
				index = find_index(LEVEL, [int(E.position.x), int(E.position.y), int(E.position.z), block_id])
				destroy(LEVELBLOCKS[block_name])
				LEVEL.pop(index)
				levelSave(LEVEL, "level.dat")
				i-=1
				print (i)
		if key == "escape":
			sys.exit()
		if key == "r":
			player.position=(5,15,5)
			"""player.enabled = False
			camera.color = color.black
			button1 = Button(texture="res/button.png", model='cube', text="Resume", text_size=0.9, highlight_color=color.light_gray, scale=(0.5, 0.2), text_color=color.white, color=color.white)
			button1.text_size = 3
			button1.on_click = Resume(button1)"""
			#button2 = ButtonQuit()


selected_block = SB(texture=id_1)
version = VERSION(text="0.0.2")

def update():
	global selected_block
	global block_id
	if held_keys['1']:
		block_id = 1
		destroy(selected_block)
		selected_block = SB(texture=id_1)
	if held_keys['2']:
		block_id = 2
		destroy(selected_block)
		selected_block = SB(texture=id_2)
	if held_keys['3']:
		block_id = 3
		destroy(selected_block)
		selected_block = SB(texture=id_3)

Sky(texture=sky_texture)
Game.run()

