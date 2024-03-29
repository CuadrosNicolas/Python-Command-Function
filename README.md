# Python Command Function

## Description

This project aims to build an easy to use package allowing to use a python function directly as a command line script using the argparse module.

When building a software, deep learning algorithm or even simple script; most of the time you will end up with one function that do all the job. But when you want to try or use it quickly you will have to use the python in command line or just edit your script each time you want to change your parameters. The best actual way for now is to use the argparse module to wrap your function with a command line interface but you will have to update it each type you change your function.

The point is that function is already what you want to call, and has already all the informations that you put in the argparse, so why not automate it ?

And this what this project is about using the function signature directly to produce an argparser.

## Installation

### Via PyPI

The project is available on PyPI and you can install using pip :
```bash
pip install autofunccli
```
### Using Github

If you want to have the example and run the tests you can clone the repository from Github.

```bash
git clone https://github.com/CuadrosNicolas/Python-Command-Function
cd pythonFunctionCommand
```

To run the test :

```bash
chmod +x ./setup.sh && setup.sh
```

Once you have done that you are ready to build your command function.

You first need to import the class from the package

```python
from autofunccli import cmdfunc
```
Then you just have to use it to wrap your function and build a command function.

## How to use

### Basic usage
```python
#examples/basic.py
from autofunccli import cmdfunc
#define a simple plus function
def plus(a,b):
	return a+b
#Use it as a main
#.main test if __name__ == '__main__'
# if it's the case, parse the command line input
out = cmdfunc(plus).main(__name__)
if(out != None):
	print(out)
```
Then you can try by running the script
```bash
python3 basic.py -h
```
Which will output :
```console
usage: basic.py [-h] a b

positional arguments:
  a           : <str>
  b           : <str>

optional arguments:
  -h, --help  show this help message and exit

[RETURN]
```
If you try it by running the script with the right arguments like if you want to add 1 and 2
```bash
python3 basic.py 1 2
```
You will end up with :
```console
12
```
But wait that's not 1+2 ! And it's normal, you have to specify that the arguments are integer to use them as integer. So let's modify the signature and add type annotation

```python
def  plus(a:int,b:int)->int:
	return a+b
```
If you run it again :
```console
3
```
Now it's the right output !
autofunccli uses the type annotation for parsing the raw input allowing a great flexibility in time if you change your signature.

Accepted type are the following :
```python
#Accepted types for function argument
acceptedTypes = [
	bool,
	int,
	float,
	str,
	List,
	Tuple
]
#Accepted types for generic type argument
acceptedTypeArgs = [
	bool,
	int,
	float,
	str
]
```
List,Tuple, Bool and Enum are special cases that you will know more about in the next section.

### Default Values
When using default value for arguments, they becomes optional argument for your command.
```python
#examples/default.py
from autofunccli import cmdfunc

def  f(must:int,optional:int=0):
	return must+optional

out = cmdfunc(f).main(__name__)
if(out != None):
	print(out)
```
### List arguments and choices
To use List and Tuple you have to import the typing package
```python
from typing import List,Tuple
```
#### List
If you want to use list as arguments like using the nargs='+' in command argparse you have to specify your function argument as a List[T] type like in this example :
```python
#examples/list.py
from autofunccli import cmdfunc
from typing import List
from functools import reduce

def  sum(l:List[int])->int:
	return reduce(lambda  prev,act:prev+act,l)

out = cmdfunc(sum).main(__name__)
if(out != None):
	print(out)
```
Will create a command like this :
```console
usage: list.py [-h] l [l ...]

positional arguments:
  l           : <List[int]>

optional arguments:
  -h, --help  show this help message and exit

[RETURN] : <int>
```
The list type argument must be in the acceptedTypeArgs array.

#### Tuple
Tuple can be seen as a special case of array with a finite number of element.
In our cases if we want to have a function taking an array of 3 numbers for example to build a color, we need to proceed like this :
```python
#examples/tuple.py
from autofunccli import cmdfunc
from typing import Tuple

def color(c:Tuple[int,int,int])->str:
	return "RGB({},{},{})".format(c[0],c[1],c[2])

out = cmdfunc(color).main(__name__)
if(out != None):
	print(out)
```
Will create a command like this :
```console
usage: tuple.py [-h] c c c

positional arguments:
  c           : <int,int,int>

optional arguments:
  -h, --help  show this help message and exit

[RETURN] : <str>
```
This command needs to have a exactly 3 integers as parameters.
Notice that you can also have different type in the Tuple type arguments.
The Tuple type arguments must be in the acceptedTypeArgs array.

#### Boolean

Boolean type can be use to produce the equivalent of the "action='store_true'" or "action='store_false'" arguments when adding argument to an arg parser.
When using a boolean type, it will automatically be an optional argument with the default False value and using the action store_true, if you specify True as a default value, the parser use the store_false action.
For example the following function :
```python
#examples/bool.py
from autofunccli import cmdfunc

def  isItTrue(b:bool):
	if(b): return  'yes'
	else: return  'no'

out = cmdfunc(isItTrue).main(__name__)
if(out != None):
	print(out)
```
Produce this result :
```console
usage: bool.py [-h] [-b]

optional arguments:
  -h, --help  show this help message and exit
  -b, --b     : <bool>(False)

[RETURN] : <str>
```
#### Choices
Choices imply that the user can only use a set of value as argument.
In our case you have to first create a class deriving from the Enum type.
And use it as a type for your argument.
The only restriction is to have the same type for each values of the Enum.
And the type be in the acceptedTypeArgs array.
```python
#you have to import the Enum class first
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
```
Produce the following command :
```console
usage: choices.py [-h] {LEFT,RIGHT}

positional arguments:
  {LEFT,RIGHT}

optional arguments:
  -h, --help    show this help message and exit

[RETURN] : <str>
```
### Merging multiple function to build command line utility

If you to build a command line utility that works like git for example. You need to use the cmdfusion class that allows to wrap multiple function and call them as one autofunccli.

For example:
```python
#examples/multifunction.py
from autofunccli import cmdfusion

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
```
Output this help :
```console
usage: multifunction.py [-h] {plus,minus}

Test with multiple function.

positional arguments:
  {plus,minus}

optional arguments:
  -h, --help    show this help message and exit

description:
        plus            plus operation
        minus           minus operation
```
In this way, the first argument allow to choose one specific command, for each one of them you can use the '-h' to print the chosen one's help.

### Document your command function
If you want to add information about your command or arguments you can use doc string that way :

```python
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
```
Produce the following command :

```console
usage: doc.py [-h] [-n] l [l ...]

Sum a list of integer.

positional arguments:
  l           List of integer. : <List[int]>

optional arguments:
  -h, --help  show this help message and exit
  -n, --n     if present, multiply the result by -1 : <bool>(False)

[RETURN] The sum of the list: <int>
```

## Author

Cuadros Nicolas


