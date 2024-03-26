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
import time
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

def ButtonSave(LEVEL, name):
	global text_save
	global isSave
	levelSave(LEVEL, name)
	player.enabled = True
	destroy(Buttons[0])
	del Buttons[0]
	destroy(Buttons[1])
	del Buttons[1]
	destroy(Buttons[2])
	del Buttons[2]
	destroy(Buttons[3])
	del Buttons[3]
	destroy(Buttons[999])
	del Buttons[999]
	isSave = 0

def ButtonLoad(LEVEL, name):
	global text_save
	global isLoad

	player.enabled = True
	destroy(Buttons[0])
	del Buttons[0]
	destroy(Buttons[1])
	del Buttons[1]
	destroy(Buttons[2])
	del Buttons[2]
	destroy(Buttons[3])
	del Buttons[3]
	destroy(Buttons[4])
	del Buttons[4]
	destroy(Buttons[999])
	del Buttons[999]
	isLoad = 0
	#scene.clear()
	if (os.path.exists(f"./levels/{name}")):
		config.set('settings', 'load-level', name)
		with open('../config.cfg', 'w') as cfg:
			config.write(cfg)
		application.quit()
	else:
		if name == 'None':
			config.set('settings', 'load-level', name)
			with open('../config.cfg', 'w') as cfg:
				config.write(cfg)
			application.quit()


BLOCKS = [
	1,
	2,
	3
]
#-----Levels Path----------
if not os.path.isdir("levels"):
    os.mkdir("levels")

#-------CONFIG-----------
config = configparser.ConfigParser()

config.add_section('settings')
config.set('settings', 'render-distance', '45')
config.set('settings', 'load-level', 'None')

if os.path.exists("../config.cfg"):
	print("true")
else:
	with open('../config.cfg', 'w') as cfg:
		config.write(cfg)
config.read('../config.cfg')
cfg_value1 = config.get('settings', 'render-distance')
cfg_value1 = int(cfg_value1)
load_level = config.get('settings', 'load-level')  


#==============GAME=============================================
app = Ursina(title="MyCraft", icon="res/stone.ico", development_mode=False, borderless = False)
window.exit_button.enabled = False
window.cog_button.enabled = False
window.fullscreen = False
window.position=Vec2(100, 100)


camera.clip_plane_far=cfg_value1

isSave = 0
isLoad = 0
bi = 0
bid = f"block_{bi}"
block_id = 1
Buttons = {}

sky_texture = load_texture("res/sky_blue.png")




if load_level == 'None':
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
else:
	if (os.path.exists(f"./levels/{load_level}")):
		LEVEL = levelLoad(f"./levels/{load_level}")
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
				for y in range(5):
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


#levelSave(LEVEL, "level.dat")
print(LEVEL)
#print (worldBlocks)
print("massive len: ", len(LEVEL))
print("dict len: ", len(LEVELBLOCKS))
player = Player()

def input(key):
		global block_id
		global bid
		global bi
		global isSave
		global isLoad

		if isSave == 0 & isLoad == 0:

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
					bi += 1

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

			if key == "escape":
				sys.exit()

			if key == "r":
				player.position=(5,15,5)
		if (isLoad == 0):
			if key == "enter":
				if isSave == 0:
					player.enabled = False
					isSave = 1
					text_save = Save(text="Save level:")
					new_button = text_save
					new_button.name = text
					Buttons[999] = new_button
					for LSave in range(4):
						if os.path.exists(f"./levels/level{LSave + 1}.dat"):
							LSAVE_text = f"level {LSave + 1}"
						else:
							LSAVE_text = '-'
						if LSave == 0:
							LSave_b = Button(text=LSAVE_text, scale=(0.5, 0.1), y=.2, texture="res/button", model='cube', color=color.white, highlight_color=color.light_gray, text_color=color.white)
							LSave_b.on_click =lambda: ButtonSave(LEVEL, './levels/level1.dat')
							new_button = LSave_b
							new_button.name = LSave
							Buttons[LSave] = new_button
						elif LSave == 1:
							LSave_b = Button(text=LSAVE_text, scale=(0.5, 0.1), y=.05, texture="res/button", model='cube', color=color.white, highlight_color=color.light_gray, text_color=color.white)
							LSave_b.on_click =lambda: ButtonSave(LEVEL, './levels/level2.dat')
							new_button = LSave_b
							new_button.name = LSave
							Buttons[LSave] = new_button
						elif LSave == 2:
							LSave_b = Button(text=LSAVE_text, scale=(0.5, 0.1), y=-.1, texture="res/button", model='cube', color=color.white, highlight_color=color.light_gray, text_color=color.white)
							LSave_b.on_click =lambda: ButtonSave(LEVEL, './levels/level3.dat')
							new_button = LSave_b
							new_button.name = LSave
							Buttons[LSave] = new_button
						elif LSave == 3:
							LSave_b = Button(text=LSAVE_text, scale=(0.5, 0.1), y=-.25, texture="res/button", model='cube', color=color.white, highlight_color=color.light_gray, text_color=color.white)
							LSave_b.on_click =lambda: ButtonSave(LEVEL, './levels/level4.dat')
							new_button = LSave_b
							new_button.name = LSave
							Buttons[LSave] = new_button
						

				else:
					player.enabled = True
					destroy(Buttons[0])
					del Buttons[0]
					destroy(Buttons[1])
					del Buttons[1]
					destroy(Buttons[2])
					del Buttons[2]
					destroy(Buttons[3])
					del Buttons[3]
					destroy(Buttons[999])
					del Buttons[999]
					isSave = 0
		if (isSave == 0):
			if key == "right shift":
				if isLoad == 0:
					player.enabled = False
					isLoad = 1
					text_save = Save(text="Load level:")
					new_button = text_save
					new_button.name = text
					Buttons[999] = new_button
					for LSave in range(5):
						if os.path.exists(f"levels/level{LSave + 1}.dat"):
							LSAVE_text = f"level {LSave + 1}"
						else:
							LSAVE_text = '-'
						if LSave == 0:
							LSave_b = Button(text=LSAVE_text, scale=(0.5, 0.1), y=.2, texture="res/button", model='cube', color=color.white, highlight_color=color.light_gray, text_color=color.white)
							LSave_b.on_click =lambda: ButtonLoad(LEVEL, 'level1.dat')
							new_button = LSave_b
							new_button.name = LSave
							Buttons[LSave] = new_button
						elif LSave == 1:
							LSave_b = Button(text=LSAVE_text, scale=(0.5, 0.1), y=.05, texture="res/button", model='cube', color=color.white, highlight_color=color.light_gray, text_color=color.white)
							LSave_b.on_click =lambda: ButtonLoad(LEVEL, 'level2.dat')
							new_button = LSave_b
							new_button.name = LSave
							Buttons[LSave] = new_button
						elif LSave == 2:
							LSave_b = Button(text=LSAVE_text, scale=(0.5, 0.1), y=-.1, texture="res/button", model='cube', color=color.white, highlight_color=color.light_gray, text_color=color.white)
							LSave_b.on_click =lambda: ButtonLoad(LEVEL, 'level3.dat')
							new_button = LSave_b
							new_button.name = LSave
							Buttons[LSave] = new_button
						elif LSave == 3:
							LSave_b = Button(text=LSAVE_text, scale=(0.5, 0.1), y=-.25, texture="res/button", model='cube', color=color.white, highlight_color=color.light_gray, text_color=color.white)
							LSave_b.on_click =lambda: ButtonLoad(LEVEL, 'level4.dat')
							new_button = LSave_b
							new_button.name = LSave
							Buttons[LSave] = new_button
						elif LSave == 4:
							LSave_b = Button(text='Defaut', scale=(0.5, 0.1), y=-.4, texture="res/button", model='cube', color=color.white, highlight_color=color.light_gray, text_color=color.white)
							LSave_b.on_click =lambda: ButtonLoad(LEVEL, 'None')
							new_button = LSave_b
							new_button.name = LSave
							Buttons[LSave] = new_button

				else:
					player.enabled = True
					destroy(Buttons[0])
					del Buttons[0]
					destroy(Buttons[1])
					del Buttons[1]
					destroy(Buttons[2])
					del Buttons[2]
					destroy(Buttons[3])
					del Buttons[3]
					destroy(Buttons[4])
					del Buttons[4]
					destroy(Buttons[999])
					del Buttons[999]
					isLoad = 0



selected_block = SB(texture=id_1)
version = VERSION(text="0.0.2_01")

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
app.run()

