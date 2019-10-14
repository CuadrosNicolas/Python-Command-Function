#examples/tuple.py
from cmdfunc import cmdfunc
from typing import Tuple

def color(c:Tuple[int,int,int])->str:
	return "RGB({},{},{})".format(c[0],c[1],c[2])

out = cmdfunc(color).main(__name__)
if(out != None):
	print(out)