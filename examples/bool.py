#examples/bool.py
from autofunccli import cmdfunc

def  isItTrue(b:bool):
	if(b): return  'yes'
	else: return  'no'

out = cmdfunc(isItTrue).main(__name__)
if(out != None):
	print(out)