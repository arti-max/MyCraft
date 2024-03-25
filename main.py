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
	1,
	2,
	3
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

bi = 0
bid = f"block_{bi}"
block_id = 1

sky_texture = load_texture("res/sky_blue.png")



if (os.path.exists("level.dat")):
	LEVEL = levelLoad("level.dat")
	for i in range(len(LEVEL)):

		bid = f"block_{bi}"

		if (LEVEL[i][3] == 0):
			block = Adminium()
		if (LEVEL[i][3] == 1):
			block = Grass()
		if (LEVEL[i][3] == 2):
			block = Stone()
		if (LEVEL[i][3] == 3):
			block = Planks()

		pos = LEVEL[i][0], LEVEL[i][1], LEVEL[i][2]
		new_block = block
		new_block.name = bid
		new_block.position = Vec3(pos)
		LEVELBLOCKS[bid] = new_block

		print (LEVEL[i])

		bi+=1
else:
	for x in range(15):
		for z in range(15):
			for y in range(4):
				bid = f"block_{bi}"
				if (y == 0):
					block = Adminium()
					generate_id = 0
				else:
					block = Grass()
					generate_id = 1
				new_block = block
				new_block.name = bid
				new_block.position = Vec3(x ,y ,z)
				LEVELBLOCKS[bid] = new_block
				levelGenerate(x, y, z, generate_id)
				bi+=1


levelSave(LEVEL, "level.dat")
print(LEVEL)
#print (worldBlocks)
print("massive len: ", len(LEVEL))
print("dict len: ", len(LEVELBLOCKS))
player = Player()

def input(key):
		global block_id
		global bid
		global bi

		if key == "right mouse down":
			A = raycast(player.position + (0, 1.5, 0), camera.forward, distance = 6, traverse_target = scene, debug=True)
			E = A.entity
			if E:
				pos = E.position + mouse.normal
				pos = tuple(pos)
				bid = f"block_{bi}"
				if block_id == 1: block = Grass()
				elif block_id == 2: block = Stone()
				elif block_id == 3: block = Planks()
				new_block = block
				new_block.name = bid
				new_block.position = pos
				LEVELBLOCKS[bid] = new_block
				LEVEL.append([int(block.x), int(block.y), int(block.z), block_id])
				levelSave(LEVEL, "level.dat")
				print("massive len: ", len(LEVEL))
				print("dict len: ", len(LEVELBLOCKS))
				bi += 1
				print (LEVEL)
				#print (bid)
		if key == "left mouse down":
			A = raycast(player.position + (0, 1.5, 0), camera.forward, distance = 6, traverse_target = scene)
			E = A.entity
			if E and E.breakable:
				block_name = E.name
				block_array = [int(E.x), int(E.y), int(E.z), E.id]
				index = find_index(LEVEL, block_array)
				destroy(LEVELBLOCKS[block_name])
				del LEVELBLOCKS[block_name]
				LEVEL.pop(index)
				levelSave(LEVEL, "level.dat")
				print(LEVEL)
				print("massive len: ", len(LEVEL))
				print("dict len: ", len(LEVELBLOCKS))
				print(index)
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

