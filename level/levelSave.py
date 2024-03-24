from ursina import *
from pickle import *
import dill

def levelSave(LEVEL, name):
	with open(name, "wb") as level:
		dill.dump(LEVEL, level)