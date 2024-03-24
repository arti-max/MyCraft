import os
import sys
from ursina import *

LEVEL = []
LEVELPOS = []
LEVELBLOCKS = {}

def levelGenerate(x ,y ,z, block_id):	
	LEVEL.append([x, y, z, block_id, 0])
	LEVELPOS.append([x, y, z])
def POSgenerate(x, y, z):
	LEVELPOS.append([x, y, z])
