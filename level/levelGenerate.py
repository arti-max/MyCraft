import os
import sys
from ursina import *

LEVEL = []
LEVELBLOCKS = {}

def levelGenerate(x, y, z, block_id):	
	LEVEL.append([x, y, z, block_id])
	print (x, y, z, block_id)
