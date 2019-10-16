#examples/multifunction.py
from cmdfunc import cmdfusion

cmd = cmdfusion("Test with multiple function.")
@cmd.add
def plus(a:int,b:int)->int:
	"""
	plus operation
	:param a: first number
	:param b: second number
	:return: a+b
	"""
	return a+b
@cmd.add
def minus(a:int,b:int)->int:
	"""
	minus operation
	:param a: first number
	:param b: second number
	:return: a-b
	"""
	return a-b

out = cmd.main(__name__)
if(out != None):
	print(out)