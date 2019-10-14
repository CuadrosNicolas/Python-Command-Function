#examples/default.py
from cmdfunc import cmdfunc

def  f(must:int,optional:int=0):
	return must+optional

out = cmdfunc(f).main(__name__)
if(out != None):
	print(out)