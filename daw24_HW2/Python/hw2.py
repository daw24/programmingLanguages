#########################################################################
# The goal of this homework is to understand and build an interpreter 	#
# in three languages (Python, SML, Java, 20 marks for each) for a small	#
# language. Your interpreter should read in an input file (input.txt)	#
# which contains lines of expressions, evaluate them and push the 	#
# results onto a stack, then print the content of the stack to an 	#
# output file (output.txt) when exit. This homework is the first of a 	#
# multi-part homework, you will be implementing some of the features. 	#
# More interesting features will be introduced in the following 	#
# homework.								# 
# Author: D. Weidenborner 	                                      	#
# 2/22/2016                                                     	#
#########################################################################

import string

# Push a number onto the stack
def push(num, inStack):
  if num[0] == '-':
    inStack.insert(0, str(0-int(num[1:])))
  elif num.isdigit():
    inStack.insert(0, str(num))
  else:
    error(inStack)

# Make top number in stack neg
def neg(inStack):
  # Check if top of stack contains a number
  if inStack[0].isdigit(): 
    negNum = inStack[0]
    inStack.remove(negNum) 
    negNum = 0 - int(negNum)
    inStack.insert(0, str(negNum))
  elif inStack[0][0] == '-':
    negNum = inStack[0]
    inStack.remove(negNum) 
    negNum = int(negNum[1:])
    inStack.insert(0, str(negNum))
  else:
    error(inStack)

# Add top two numbers on stack
def add(inStack):
  # Check if top two elements on stack are integer numbers
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0].isdigit() or inStack[0][0] == '-') and 
        (inStack[1].isdigit() or inStack[1][0] == '-')):
    num1 = inStack[0]
    inStack.remove(num1)
    num2 = inStack[0]
    inStack.remove(num2)
    total = int(num1) + int(num2)
    inStack.insert(0, str(total))
  else:
    error(inStack)

def mul(inStack):
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0].isdigit() or inStack[0][0] == '-') and 
        (inStack[1].isdigit() or inStack[1][0] == '-')):
    num1 = inStack[0]
    inStack.remove(num1)
    num2 = inStack[0]
    inStack.remove(num2)
    total = int(num1) * int(num2)
    inStack.insert(0, str(total))
  else:
    error(inStack)

def sub(inStack):
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0].isdigit() or inStack[0][0] == '-') and 
        (inStack[1].isdigit() or inStack[1][0] == '-')):
    num1 = inStack[0]
    inStack.remove(num1)
    num2 = inStack[0]
    inStack.remove(num2)
    total = int(num2) - int(num1)
    inStack.insert(0, str(total))
  else:
    error(inStack)

def div(inStack):
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0].isdigit() or inStack[0][0] == '-') and 
        (inStack[1].isdigit() or inStack[1][0] == '-')):
    if inStack[0] == '0':
      error(inStack)
    else: 
      num1 = inStack[0]
      inStack.remove(num1)
      num2 = inStack[0]
      inStack.remove(num2)
      total = int(num2) / int(num1)
      inStack.insert(0, str(int(total)))
  else:
    error(inStack)

def rem(inStack):
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0].isdigit() or inStack[0][0] == '-') and 
        (inStack[1].isdigit() or inStack[1][0] == '-')):
    if inStack[0] == '0':
      error(inStack)
    else: 
      num1 = inStack[0]
      inStack.remove(num1)
      num2 = inStack[0]
      inStack.remove(num2)
      total = int(num2) % int(num1)
      inStack.insert(0, str(int(total)))
  else:
    error(inStack)

def true(inStack):
  inStack.insert(0, ':true:')

def false(inStack):
  inStack.insert(0, ':false:')

def pop(inStack):
  if len(inStack) > 0:
    inStack.pop(0)
  else:
    error(inStack)

def swap(inStack):
  if len(inStack) < 2:
   error(inStack)
  else:
    inStack.insert(0, str(inStack.pop(1)))

def error(inStack):
  inStack.insert(0, ':error:')


# Checks the expression 
def checkExp(inString, inStack):
  splitStr = inString.split()
  if splitStr[0] == 'push':
    push(splitStr[1], inStack)
  elif splitStr[0] == 'neg':
    neg(inStack)
  elif splitStr[0] == 'add':
    add(inStack)
  elif splitStr[0] == 'mul':
    mul(inStack)
  elif splitStr[0] == 'sub':
    sub(inStack)
  elif splitStr[0] == 'div':
    div(inStack)
  elif splitStr[0] == ':true:':
    true(inStack)
  elif splitStr[0] == ':false:':
    false(inStack)
  elif splitStr[0] == 'pop':
    pop(inStack)
  elif splitStr[0] == 'swap':
    swap(inStack)
  elif splitStr[0] == 'rem':
    rem(inStack)

def hw2(input, output):
  # Read input file line by line
  f = open(input, 'r')
  strings = []
  for line in f:
    strings.append(line)
  f.close()

  stack = []

  for string in strings:
    splitString = string.split()
    if string == '\n':
      continue
    elif(splitString[0] == 'quit'):
      # Wtire result to output file
      f = open(output, 'w')
      for element in stack:
        f.write(str(element))
        f.write('\n')
      f.close()
      return;
    else:
      checkExp(string, stack) 

#hw2('input.txt', 'output.txt')

