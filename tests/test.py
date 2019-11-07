import unittest
from autofunccli import cmdfunc,UnsupportedTypeException,WrongInputTypeException,NonHomogenousEnumTypeException,EnumHasNoTypeException,cmdfusion
from typing import Tuple,List
from enum import Enum
from functools import reduce

class TestCmdFunc(unittest.TestCase):

	def test_basic(self):
		def plus(a,b):
			return a+b
		def plusTyped(a:int,b:int)->int:
			return a+b
		assert cmdfunc(plus).parse(['1','1']) == '11'
		assert cmdfunc(plusTyped).parse(['1','1']) == 2

	def test_boolean(self):
		def  isItTrue(b:bool):
			if(b): return  'yes'
			else: return  'no'
		assert cmdfunc(isItTrue).parse([]) == 'no'
		assert cmdfunc(isItTrue).parse(['-b']) == 'yes'

		def  isItTrueWithDefault(b:bool=True):
			if(b): return  'yes'
			else: return  'no'
		assert cmdfunc(isItTrueWithDefault).parse([]) == 'yes'
		assert cmdfunc(isItTrueWithDefault).parse(['-b']) == 'no'

	def test_choices(self):
		class LEFT_OR_RIGHT(Enum):
			LEFT  =  'LEFT'
			RIGHT  =  'RIGHT'
		def  whereAreYouGoing(d:LEFT_OR_RIGHT)->str:
			if(d==LEFT_OR_RIGHT.LEFT):
				return  'GOING LEFT !'
			elif(d==LEFT_OR_RIGHT.RIGHT):
				return  'GOING RIGHT'
		assert cmdfunc(whereAreYouGoing).parse(['LEFT']) == 'GOING LEFT !'
		assert cmdfunc(whereAreYouGoing).parse(['RIGHT']) == 'GOING RIGHT'

	def test_default(self):
		def  f(must:int,optional:int=0):
			return must+optional
		assert cmdfunc(f).parse(['1']) == 1
		assert cmdfunc(f).parse(['1','-o','2']) == 3
		assert cmdfunc(f).parse(['1','--optional','2']) == 3

	def test_list(self):
		def  sum(l:List[int])->int:
			return reduce(lambda  prev,act:prev+act,l)
		assert cmdfunc(sum).parse(['1','2','3']) == 6

	def test_tuple(self):
		def color(c:Tuple[int,int,int])->str:
			return "RGB({},{},{})".format(c[0],c[1],c[2])
		assert cmdfunc(color).parse(['1','2','3']) == 'RGB(1,2,3)'

	def test_enum(self):
		#TEST NON HOMOGENOUS
		class nonHomogenous(Enum):
			a = 1
			b = '2'
		def nonHomogenousFunc(t:nonHomogenous):
			pass
        # check that s.split fails when the separator is not a string
		with self.assertRaises(NonHomogenousEnumTypeException):
			cmdfunc(nonHomogenousFunc)

		#TEST NO TYPE
		class noType(Enum):
			pass
		def noTypeFunc(t:noType):
			pass
        # check that s.split fails when the separator is not a string
		with self.assertRaises(EnumHasNoTypeException):
			cmdfunc(noTypeFunc)

	def test_input(self):
		def integer(i:int):
			return i
		with self.assertRaises(WrongInputTypeException):
			cmdfunc(integer).parse(['a'])

	def test_unsupportedType(self):
		class T:
			pass
		def unsupType(i:T):
			pass
		def unsupTypeArg(i:List[T]):
			pass
		with self.assertRaises(UnsupportedTypeException):
			cmdfunc(unsupType)
		with self.assertRaises(UnsupportedTypeException):
			cmdfunc(unsupTypeArg)

	def test_multifunction(self):
		cmd = cmdfusion("Test with multiple function.")
		@cmd.add
		def plus(a:int,b:int)->int:
			return a+b
		@cmd.add
		def minus(a:int,b:int)->int:
			return a-b
		assert cmd.parse('plus','1','2')==3
		assert cmd.parse(['minus','2','1'])==1
if __name__ == '__main__':
	unittest.main()
