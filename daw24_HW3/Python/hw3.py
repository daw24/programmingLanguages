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
# 4/12/2016                                                     	#
#########################################################################

import string

# Push a number onto the stack
def push(exp, inStack):
  if exp[0] == '-' and exp[1:].isdigit():
    inStack.insert(0, str(0-int(exp[1:])))
  elif exp[0] == '"':
    inStack.insert(0, str(exp))
    #inStack.insert(0, str(exp[1:(len(exp)-1)]))
    #print(exp[1])
    #print(exp[1].isdigit())
  elif exp.isdigit():
    inStack.insert(0, str(exp))
  elif exp[0].isalpha():
    inStack.insert(0, exp)
  else:
    error(inStack)

# Make top number in stack neg
def neg(inStack, inBinds):
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
  # check for bindings
  elif inStack[0] in inBinds:
    negNum = inBinds[inStack[0]]
    if negNum.isdigit():
      inStack.remove(inStack[0])
      negNum = 0 - int(negNum)
      inStack.insert(0, str(negNum))
    elif negNum[0] == '-':
      inStack.remove(inStack[0])
      negNum = int(negNum[1:])
      inStack.inster(0, str(negNum))
    else: error(inStack)
  else:
    error(inStack)

def isNumInBinds(exp, inBinds):
  #print(exp)
  if exp in inBinds:
    #print("exp in binds")
    num = inBinds[exp]
    if (num.isdigit() or num[0] == '-'):
      return True
  else: return False

# Add top two numbers on stack
def add(inStack, inBinds):
  # Check if top two elements on stack are integer numbers
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0].isdigit() or inStack[0][0] == '-' or isNumInBinds(inStack[0], inBinds)) and 
        (inStack[1].isdigit() or inStack[1][0] == '-' or isNumInBinds(inStack[1], inBinds))):
    num1 = inStack[0]
    #prevElement = inStack[0]
    if num1 in inBinds:
      num1 = inBinds[inStack[0]]
      #if (num1.isdigit() or num1[0] == '='):
      inStack.remove(inStack[0])     
      #else:
       # print("#1 inBinds not a number")
        #error(inStack)
    else:
      inStack.remove(num1)
    num2 = inStack[0]
    if num2 in inBinds:
      num2 = inBinds[inStack[0]]
      #if (num2.isdigit() or num2[0] == '='):
      inStack.remove(inStack[0])
      #else:
       # inStack.insert(0, prevElement)
        #print("#2 inBinds not a number")
        #error(inStack)
    else:
      inStack.remove(num2)
    total = int(num1) + int(num2)
    inStack.insert(0, str(total))
  else:
    error(inStack)

def mul(inStack, inBinds):
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0].isdigit() or inStack[0][0] == '-' or isNumInBinds(inStack[0], inBinds)) and 
        (inStack[1].isdigit() or inStack[1][0] == '-' or isNumInBinds(inStack[1], inBinds))):
    num1 = inStack[0]
    if num1 in inBinds:
      num1 = inBinds[inStack[0]]
      inStack.remove(inStack[0])     
    else:
      inStack.remove(num1)
    num2 = inStack[0]
    if num2 in inBinds:
      num2 = inBinds[inStack[0]]
      inStack.remove(inStack[0])
    else:
      inStack.remove(num2)
    total = int(num1) * int(num2)
    inStack.insert(0, str(total))
  else:
    error(inStack)

def sub(inStack, inBinds):
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0].isdigit() or inStack[0][0] == '-' or isNumInBinds(inStack[0], inBinds)) and 
        (inStack[1].isdigit() or inStack[1][0] == '-' or isNumInBinds(inStack[1], inBinds))):
    num1 = inStack[0]
    if num1 in inBinds:
      num1 = inBinds[inStack[0]]
      inStack.remove(inStack[0])     
    else:
      inStack.remove(num1)
    num2 = inStack[0]
    if num2 in inBinds:
      num2 = inBinds[inStack[0]]
      inStack.remove(inStack[0])
    else:
      inStack.remove(num2)
    total = int(num2) - int(num1)
    inStack.insert(0, str(total))
  else:
    error(inStack)

def div(inStack, inBinds):
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0].isdigit() or inStack[0][0] == '-' or isNumInBinds(inStack[0], inBinds)) and 
        (inStack[1].isdigit() or inStack[1][0] == '-' or isNumInBinds(inStack[1], inBinds))):
    num1 = inStack[0]
    element1 = inStack[0]
    if num1 in inBinds:
      num1 = inBinds[inStack[0]]
      inStack.remove(inStack[0])     
    else:
      inStack.remove(num1)
    num2 = inStack[0]
    element2 = inStack[0]
    if num2 in inBinds:
      num2 = inBinds[inStack[0]]
      inStack.remove(inStack[0])
    else:
      inStack.remove(num2)
      if int(num1) == 0:
        inStack.insert(0, element2)
        inStack.insert(0, element1)
        error(inStack)
      else:
        total = int(num2) / int(num1)
        inStack.insert(0, str(int(total)))
  else:
    error(inStack)

def rem(inStack, inBinds):
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0].isdigit() or inStack[0][0] == '-' or isNumInBinds(inStack[0], inBinds)) and 
        (inStack[1].isdigit() or inStack[1][0] == '-' or isNumInBinds(inStack[1], inBinds))):
    num1 = inStack[0]
    element1 = inStack[0]
    if num1 in inBinds:
      num1 = inBinds[inStack[0]]
      inStack.remove(inStack[0])     
    else:
      inStack.remove(num1)
    num2 = inStack[0]
    element2 = inStack[0]
    if num2 in inBinds:
      num2 = inBinds[inStack[0]]
      inStack.remove(inStack[0])
    else:
      inStack.remove(num2)
      if int(num1) == 0:
        inStack.insert(0, element2)
        inStack.insert(0, element1)
        error(inStack)
      else:
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

def isNotBoolInBinds(exp, inBinds):
  if exp in inBinds:
    bool1 = inBinds[exp]
    if (bool1 != ':true:' and bool1 != ':false:'):
      return True
    else: return False
  else: return True

def andMethod(inStack, inBinds):
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0] != ':true:' and inStack[0] != ':false:' and isNotBoolInBinds(inStack[0], inBinds)) or
	(inStack[1] != ':true:' and inStack[1] != ':false:' and isNotBoolInBinds(inStack[1], inBinds))):
    error(inStack)
  else:
    bool1 = inStack[0]
    if bool1 in inBinds:
      bool1 = inBinds[inStack[0]]
      inStack.remove(inStack[0])
    else:
      inStack.remove(bool1)
    bool2 = inStack[0]
    if bool2 in inBinds:
      bool2 = inBinds[inStack[0]]
      inStack.remove(inStack[0])
    else:
      inStack.remove(bool2)
    if(bool1 == ':true:' and bool2 == ':true:'):
      inStack.insert(0, ':true:')
    else:
      inStack.insert(0, ':false:')

def orMethod(inStack, inBinds):
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0] != ':true:' and inStack[0] != ':false:' and isNotBoolInBinds(inStack[0], inBinds)) or
	(inStack[1] != ':true:' and inStack[1] != ':false:' and isNotBoolInBinds(inStack[1], inBinds))):
    error(inStack)
  else:
    bool1 = inStack[0]
    if bool1 in inBinds:
      bool1 = inBinds[inStack[0]]
      inStack.remove(inStack[0])
    else:
      inStack.remove(bool1)
    bool2 = inStack[0]
    if bool2 in inBinds:
      bool2 = inBinds[inStack[0]]
      inStack.remove(inStack[0])
    else:
      inStack.remove(bool2)
    if(bool1 == ':true:' or bool2 == ':true:'):
      inStack.insert(0, ':true:')
    else:
      inStack.insert(0, ':false:')

def ifMethod(inStack, inBinds):
  if len(inStack) < 3:
    error(inStack)
  elif (inStack[2] != ':true:' and inStack[2] != ':false:' and isNotBoolInBinds(inStack[2], inBinds)):
    error(inStack)
  else:
    #bool1 = inStack[0]
    #if bool1 in inBinds:
     # bool1 = inBinds[inStack[0]]
     # inStack.remove(inStack[0])
    #else:
     # inStack.remove(bool1)
    #bool2 = inStack[0]
   # if bool2 in inBinds:
    #  bool2 = inBinds[inStack[0]]
     # inStack.remove(inStack[0])
    #else:
     # inStack.remove(bool2)
    bool3 = inStack[2]
    if bool3 in inBinds:
      bool3 = inBinds[inStack[2]]
      inStack.remove(inStack[2])
    else:
      inStack.remove(bool3)
    if bool3 == ':true:':
      inStack.remove(inStack[1])
      #nStack.insert(0, bool1)
    else:
      inStack.remove(inStack[0])
      #inStack.insert(0, bool2)

def notMethod(inStack, inBinds):
  if len(inStack) < 1:
    error(inStack)
  elif (inStack[0] != ':true:' and inStack[0] != ':false:' and isNotBoolInBinds(inStack[0], inBinds)):
    error(inStack)
  else:
    bool1 = inStack[0]
    if bool1 in inBinds:
      bool1 = inBinds[inStack[0]]
      inStack.remove(inStack[0])
    else:
      inStack.remove(bool1)
    if(bool1 == ':true:'):
      inStack.insert(0, ':false:')
    else:
      inStack.insert(0, ':true:')

def equal(inStack, inBinds):
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0].isdigit() or inStack[0][0] == '-' or isNumInBinds(inStack[0], inBinds)) and 
        (inStack[1].isdigit() or inStack[1][0] == '-' or isNumInBinds(inStack[1], inBinds))):
    num1 = inStack[0]
    if num1 in inBinds:
      num1 = inBinds[inStack[0]]
      inStack.remove(inStack[0])     
    else:
      inStack.remove(num1)
    num2 = inStack[0]
    if num2 in inBinds:
      num2 = inBinds[inStack[0]]
      inStack.remove(inStack[0])
    else:
      inStack.remove(num2)
    if( int(num2) == int(num1)):
      inStack.insert(0, ':true:')
    else:
      inStack.insert(0, ':false:')
  else:
    error(inStack)

def lessThan(inStack, inBinds):
  if len(inStack) < 2:
    error(inStack)
  elif ((inStack[0].isdigit() or inStack[0][0] == '-' or isNumInBinds(inStack[0], inBinds)) and 
        (inStack[1].isdigit() or inStack[1][0] == '-' or isNumInBinds(inStack[1], inBinds))):
    num1 = inStack[0]
    if num1 in inBinds:
      num1 = inBinds[inStack[0]]
      inStack.remove(inStack[0])     
    else:
      inStack.remove(num1)
    num2 = inStack[0]
    if num2 in inBinds:
      num2 = inBinds[inStack[0]]
      inStack.remove(inStack[0])
    else:
      inStack.remove(num2)
    if( int(num2) < int(num1)):
      inStack.insert(0, ':true:')
    else:
      inStack.insert(0, ':false:')
  else:
    error(inStack)

def bind(inStack, inBinds):
  if len(inStack) < 2:
    error(inStack)
  elif(not inStack[1][0].isalpha() or inStack[0] == ':error:'):
    error(inStack)
  else:
    var = inStack[0]
    inStack.remove(var)
    varName = inStack[0]
    inStack.remove(varName)
    if var in inBinds:
      inBinds[varName] = inBinds[var]   
    else:
      inBinds[varName] = var
    inStack.insert(0, ':unit:')
    #print("keys are ", inBinds.keys())

def let(inStack, inBinds):
  inStack.insert(0, '""let"')

def end(inStack, inBinds):  
  index = inStack.index('""let"')
  while(index > 0):
    inStack.pop(index)
    index -= 1

# Checks the expression 
def checkExp(inString, inStack, inBinds):
  splitStr = inString.split()
  if splitStr[0] == 'push':
    push(splitStr[1], inStack)
  elif splitStr[0] == 'neg':
    neg(inStack, inBinds)
  elif splitStr[0] == 'add':
    add(inStack, inBinds)
  elif splitStr[0] == 'mul':
    mul(inStack, inBinds)
  elif splitStr[0] == 'sub':
    sub(inStack, inBinds)
  elif splitStr[0] == 'div':
    div(inStack, inBinds)
  elif splitStr[0] == ':true:':
    true(inStack)
  elif splitStr[0] == ':false:':
    false(inStack)
  elif splitStr[0] == 'pop':
    pop(inStack)
  elif splitStr[0] == 'swap':
    swap(inStack)
  elif splitStr[0] == 'rem':
    rem(inStack, inBinds)
  elif splitStr[0] == ':error:':
    error(inStack)
  elif splitStr[0] == 'and':
    andMethod(inStack, inBinds)
  elif splitStr[0] == 'or':
    orMethod(inStack, inBinds)
  elif splitStr[0] == 'not':
    notMethod(inStack, inBinds)
  elif splitStr[0] == 'equal':
    equal(inStack, inBinds)
  elif splitStr[0] == 'lessThan':
    lessThan(inStack, inBinds)
  elif splitStr[0] == 'bind':
    bind(inStack, inBinds)
  elif splitStr[0] == 'if':
    ifMethod(inStack, inBinds)
  elif splitStr[0] == 'let':
    let(inStack, inBinds)
  elif splitStr[0] == 'end':
    end(inStack, inBinds)


def hw3(input, output):
  # Read input file line by line
  f = open(input, 'r')
  strings = []
  for line in f:
    strings.append(line)
  f.close()

  stack = []
  binds = {}
  for string in strings:
    splitString = string.split()
    if string == '\n':
      continue
    elif(splitString[0] == 'quit'):
      # Write result to output file
      f = open(output, 'w')
      for element in stack:
        if element[0] == '"':
          # Remove quotations from literal string elements
          f.write(str(element[1:(len(element)-1)]))
          f.write('\n')
        else:
          f.write(str(element))
          f.write('\n')
      f.close()
      return;
    else:
      checkExp(string, stack, binds)

#hw3('input.txt', 'output.txt')

