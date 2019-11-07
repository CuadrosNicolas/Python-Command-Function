#examples/doc.py
from autofunccli import cmdfunc
from typing import List
from functools import reduce

def  sum(l:List[int],n:bool)->int:
	"""
	Sum a list of integer.
	:param l: List of integer.
	:param n: if present, multiply the result by -1
	:return: The sum of the list
	"""
	o =  reduce(lambda  prev,act:prev+act,l)
	if(n):o*=-1
	return o

out = cmdfunc(sum).main(__name__)
if(out != None):
	print(out)