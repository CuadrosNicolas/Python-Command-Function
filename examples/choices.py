#examples/choices.py
from autofunccli import cmdfunc

#you have to import the Enum class first
from enum import Enum
class LEFT_OR_RIGHT(Enum):
	LEFT  =  'LEFT'
	RIGHT  =  'RIGHT'
def  whereAreYouGoing(d:LEFT_OR_RIGHT)->str:
	if(d==LEFT_OR_RIGHT.LEFT):
		return  'GOING LEFT !'
	elif(d==LEFT_OR_RIGHT.RIGHT):
		return  'GOING RIGHT'

out = cmdfunc(whereAreYouGoing).main(__name__)
if(out != None):
	print(out)