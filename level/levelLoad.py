from ursina import *
import pickle

def levelLoad(name):
	if (os.path.exists(name)):
		with open(name, "rb") as level:
			LEVEL = pickle.load(level)
			return LEVEL
	else:
		return False