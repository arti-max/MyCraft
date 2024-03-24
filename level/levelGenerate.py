import os
import sys
from ursina import *

LEVEL = []
LEVELPOS = []
LEVELBLOCKS = {}

def levelGenerate(pos, block_id):	
	LEVEL.append([pos, block_id, 0])
	LEVELPOS.append([pos])
def POSgenerate(pos):
	LEVELPOS.append([pos])
