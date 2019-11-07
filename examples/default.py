#examples/default.py
from autofunccli import cmdfunc

def  f(must:int,optional:int=0):
	return must+optional

out = cmdfunc(f).main(__name__)
if(out != None):
	print(out)