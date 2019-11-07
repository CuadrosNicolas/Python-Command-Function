#examples/basic.py
from autofunccli import cmdfunc
#define a simple plus function
def plus(a:int,b:int)->int:
	return a+b
#Use it as a main
#.main test if __name__ == '__main__'
# if it's the case, parse the command line input
out = cmdfunc(plus).main(__name__)
if(out != None):
	print(out)