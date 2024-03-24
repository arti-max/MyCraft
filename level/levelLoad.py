from ursina import *
import dill

def levelLoad(name):
	if (os.path.exists(name)):
		with open(name, "rb") as level:
			LEVEL = dill.load(level)
			return LEVEL
	else:
		return False