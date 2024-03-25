from ursina import *
import pickle

def levelSave(LEVEL, name):
	with open(name, "wb") as level:
		pickle.dump(LEVEL, level)