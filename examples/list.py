#examples/list.py
from cmdfunc import cmdfunc
from typing import List
from functools import reduce

def  sum(l:List[int])->int:
	return reduce(lambda  prev,act:prev+act,l)

out = cmdfunc(sum).main(__name__)
if(out != None):
	print(out)