import re
import copy
fInput = 0
def hw4(input, output):
    global fInput
    fInput = open(input,'r')
    f = open(output,'w')
    stack = []
    hm = {}
    closures = {}
    funStack = []
    for line in fileRead():
        #print(line)
        if line.startswith('let'):
            stack.insert(0,parseLet(fInput,copy.deepcopy(hm),f, closures))
        elif line.startswith('fun '):
            splitString = line.split()
            #stack.insert(0,parseFun(fInput,copy.deepcopy(hm),f, splitString, closures))
            stack.insert(0,parseFun(fInput,copy.deepcopy(hm),f, splitString, closures, 0))
        elif line.startswith('inOut'):
            splitString = line.split()
            #stack.insert(0,parseFun(fInput,copy.deepcopy(hm),f, splitString, closures))
            stack.insert(0,parseFun(fInput,copy.deepcopy(hm),f, splitString, closures, 1))

        elif line.startswith('call'):
            if stack[1] == ':error:':
                stack.insert(0, ':error:')
            else:
                argValueOriginal = stack[1]
                funName = stack[0]
                argValue = stack[1]
                if funName not in closures:
                    stack.insert(0, ':error:')
                    #print('error')
                    continue
                stack.pop(0)
                stack.pop(0)
                #print('reached')
                stack.insert(0,parseCall(fInput,copy.deepcopy(hm),f, closures, funName, argValue))
                #print('stack: ', stack)
                #print('flag: ', closures[funName][-2], ' ', argValueOriginal, ' ', stack[0]) 
                if len(stack) > 0 and closures[funName][-2] == 1:
                    hm[argValueOriginal] = stack[0]
        elif line[0].isalpha():
            parsePrimitive(line, stack, hm, f)
        elif line[0] == ':':
            parseBooleanOrError(line, stack, hm)
    fInput.close()

def fileRead():
   for line in fInput:
        yield line 

def parseLet(input,hm_parent,f, closures):
    global fInput
    stack_let = []
    hm_let = hm_parent
    for line in fileRead():
        #print('let: ', line)
        if line.startswith('end'):
            return stack_let[0]
        elif line.startswith('let'):
            stack_let.insert(0,parseLet(fInput,copy.deepcopy(hm_let),f, closures))
        elif line.startswith('fun '):
            splitString = line.split()
            stack_let.insert(0,parseFun(fInput,copy.deepcopy(hm_let),f, splitString, closures, 0))
        elif line.startswith('inOut'):
            splitString = line.split()
            stack_let.insert(0,parseFun(fInput,copy.deepcopy(hm_let),f, splitString, closures, 1))
        elif line.startswith('call'):
            if stack_let[1] == ':error:':
                stack_let.insert(0, ':error:')
            else:
                funName = stack_let[0]
                argValue = stack_let[1]
                if funName not in closures:
                    stack_let.insert(0, ':error:')
                    continue
                stack_let.pop(0)
                stack_let.pop(0)
                stack_let.insert(0,parseCall(fInput,copy.deepcopy(hm_let),f, closures, funName, argValue))
        elif line[0].isalpha():
            parsePrimitive(line, stack_let, hm_let, f)
        elif line[0] == ':':
            parseBooleanOrError(line, stack_let, hm_let)

def parseFun(input,hm_parent,f, funLine, closures, flag):
    global fInput
    stack_fun = []
    hm_fun = hm_parent
    funName = funLine[1]
    funArg = funLine[2]
    for line in fileRead():
        #print(line)
        if line.startswith('funEnd'):
            stack_fun.append(flag)
            stack_fun.append(funArg)
            closures[funName] = stack_fun
            closures[funName+'_hm'] = hm_fun
            #print("Closures : ", closures)
            #tempStack = funStack
            return ':unit:'
        elif line.startswith('fun '):
            parseFun(fInput,copy.deepcopy(hm_fun),f)
        else:
             stack_fun.append(line.rstrip())
        #elif line[0].isalpha():
            #parsePrimitive(line, stack_fun, hm_fun, f)
        #elif line[0] == ':':
            #parseBooleanOrError(line, stack_fun, hm_fun)

def parseCall(input,hm_parent,f,closures,funName,argValue):
    global fInput
    stack_call = []
    hm_call = hm_parent
    hm_fun = closures[funName+'_hm']
    # add diction from function to dictionary from call; fun keys overwrite call keys
    hm_combine = hm_call.copy()
    hm_combine.update(hm_fun)
    #print('dictionary at call: ', hm_call)
    function = closures[funName]
    if argValue in hm_call:
        argValue = hm_call[argValue]
    #if argValue in closures:
    #    argValue = closures[argValue]
    #print('functionArg: ', function[-1], ' = ', argValue, ', argValue')
    hm_combine[function[-1]] = argValue
    for line in function:
        #print('function line is: ', line)
        if line == 0 or line == 1:
            #print('breaking')
            break
        elif line.startswith('return'):
            if stack_call[0] in hm_combine: 	#hm_call
                return hm_combine[stack_call[0]]
            else:
                return stack_call[0]
        elif line.startswith('fun'):
            stack_call.insert(0,parseFun(fInput,copy.deepcopy(hm_combine),f, closures))	#hm_call
        #elif line.startswith('let'):
        #    stack_call.insert(0,parseLet(fInput,copy.deepcopy(hm_combine),f, closures))	#hm_call
        elif line.startswith('call'):
            if stack_call[1] == ':error:':
                stack_call.insert(0, ':error:')
            else:
                funName = stack_call[0]
                argValue = stack_call[1]
                stack_call.pop(0)
                stack_call.pop(0)
                if funName in hm_combine:
                    funName = hm_combine[funName]
                stack_call.insert(0,parseCall(fInput,copy.deepcopy(hm_combine),f, closures, funName, argValue))
                #stack_call.insert(0,parseCall(copy.deepcopy(hm_combine),f, closures, stack_call[0], stack_call[1]))
        elif line[0].isalpha():
            parsePrimitive(line, stack_call, hm_combine, f)	#hm_call
        elif line[0] == ':':
            parseBooleanOrError(line, stack_call, hm_combine)	#hm_call

def parsePrimitive(line, stack, hm, f):
    if line.startswith('add'):
        doAdd(stack, hm)
    elif line.startswith('sub'):
        doSub(stack, hm)
    elif line.startswith('mul'):
        doMul(stack, hm)
    elif line.startswith('div'):
        doDiv(stack, hm)
    elif line.startswith('rem'):
        doRem(stack, hm)
    elif line.startswith('pop'):
        doPop(stack)
    elif line.startswith('push'):
        doPush(stack, line)
    elif line.startswith('swap'):
        doSwap(stack)
    elif line.startswith('neg'):
        doNeg(stack, hm)
    elif line.startswith('quit'):
        doQuit(stack, f, hm)
    elif line.startswith('if'):
        doIf(stack, hm)
    elif line.startswith('not'):
        doNot(stack, hm)
    elif line.startswith('and'):
        doAnd(stack, hm)
    elif line.startswith('or'):
        doOr(stack, hm)
    elif line.startswith('equal'):
        doEqual(stack, hm)
    elif line.startswith('lessThan'):
        doLessThan(stack, hm)
    elif line.startswith('bind'):
        doBind(stack, hm)

def doAdd(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            stack.pop(0)
            stack.pop(0)
            newTop = x+y
            return stack.insert(0, str(newTop))
        else:
            return stack.insert(0, ':error:')


def doSub(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            stack.pop(0)
            stack.pop(0)
            newTop = x-y
            return stack.insert(0, str(newTop))
        else:
            return stack.insert(0, ':error:')



def doMul(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            stack.pop(0)
            stack.pop(0)
            newTop = x*y
            return stack.insert(0, str(newTop))
        else:
            return stack.insert(0, ':error:')



def doDiv(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            if y == 0:
                return stack.insert(0, ':error:')
            stack.pop(0)
            stack.pop(0)
            newTop = x//y
            return stack.insert(0, str(newTop))
        else:
            return stack.insert(0, ':error:')



def doRem(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            if y == 0:
                return stack.insert(0, ':error:')
            stack.pop(0)
            stack.pop(0)
            newTop = x%y
            return stack.insert(0, str(newTop))
        else:
            return stack.insert(0, ':error:')


def doPop(stack):
    if len(stack) < 1:
        return stack.insert(0, ':error:')
    else:
        return stack.pop(0)


def doPush(stack, line):
    getList = line.split(' ',1)
    getList[1] = getList[1].strip('\n')
    if getList[1][0] == '-':
        if getList[1][1:] == '0':
            return stack.insert(0,'0')
        elif getList[1][1:].isdigit():
            return stack.insert(0, getList[1])
        else:
            return stack.insert(0, ':error:')
    elif getList[1].isdigit():
        return stack.insert(0, getList[1])
    elif re.match('^[a-zA-Z].*',getList[1],0):
        return stack.insert(0, getList[1])
    elif re.match('^".+"$',getList[1],0):
        return stack.insert(0, getList[1])
    else:
        return stack.insert(0, ':error:')


def doSwap(stack):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    else:
        x = stack[1]
        y = stack[0]
        stack.pop(0)
        stack.pop(0)
        stack.insert(0, y)
        return stack.insert(0, x)



def doNeg(stack, hm):
    if len(stack) < 1:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if s0.isdigit:
            x = int(s0)
            stack.pop(0)
            newTop = -1*x
            return stack.insert(0, str(newTop))
        else:
            return stack.insert(0, ':error:')


def doQuit(stack, f, hm):
    #print('QUIT reached')
    for ele in stack:
        #ele = str(hm.get(ele,ele))
        f.write(ele.strip('"') + '\n')
    f.close()

def parseBooleanOrError(line, stack, hm):
    if line[1] == 'e':
        return stack.insert(0,':error:')
    elif line[1] == 't':
        return stack.insert(0,':true:')
    else:
        return stack.insert(0,':false:')

def doIf(stack, hm):
    if len(stack) < 3:
        return stack.insert(0, ':error:')
    else:
        s2 = str(stack[2])
        if s2 != ':true:' and s2 != ':false:':
            s2 = str(hm.get(s2,s2))
        if s2 == ':true:':
            stack.pop(2)
            stack.pop(1)
            return stack
        elif s2 == ':false:':
            stack.pop(2)
            stack.pop(0)
            return stack
        else:
            return stack.insert(0,':error:')

def doNot(stack, hm):
    if len(stack) < 1:
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        if s0 != ':true:' and s0 != ':false:':
            s0 = str(hm.get(s0,s0))
        if s0 == ':true:':
            stack.pop(0)
            stack.insert(0,':false:')
            return stack
        elif s0 == ':false:':
            stack.pop(0)
            stack.insert(0,':true:')
            return stack
        else:
            return stack.insert(0,':error:')
        
def doAnd(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if s0 != ':true:' and s0 != ':false:':
            s0 = str(hm.get(s0,s0))
        if s1 != ':true:' and s1 != ':false:':
            s1 = str(hm.get(s1,s1))
        if s0 == ':false:' and s1 == ':false:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':false:')
            return stack
        elif s0 == ':false:' and s1 == ':true:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':false:')
            return stack
        elif s0 == ':true:' and s1 == ':false:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':false:')
            return stack
        elif s0 == ':true:' and s1 == ':true:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':true:')
            return stack
        else:
            return stack.insert(0,':error:')
        
def doOr(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if s0 != ':true:' and s0 != ':false:':
            s0 = str(hm.get(s0,s0))
        if s1 != ':true:' and s1 != ':false:':
            s1 = str(hm.get(s1,s1))
        if s0 == ':false:' and s1 == ':false:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':false:')
            return stack
        elif s0 == ':false:' and s1 == ':true:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':true:')
            return stack
        elif s0 == ':true:' and s1 == ':false:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':true:')
            return stack
        elif s0 == ':true:' and s1 == ':true:':
            stack.pop(0)
            stack.pop(0)
            stack.insert(0,':true:')
            return stack
        else:
            return stack.insert(0,':error:')
        
def doEqual(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            stack.pop(0)
            stack.pop(0)
            if x==y:
                return stack.insert(0, ':true:')
            else:
                return stack.insert(0, ':false:')
        else:
            return stack.insert(0, ':error:')
        
def doLessThan(stack, hm):
    if len(stack) < 2:
        return stack.insert(0, ':error:')
    elif stack[0][0] == ':' or stack[1][0] == ':':
        return stack.insert(0, ':error:')
    else:
        s0 = str(stack[0])
        s1 = str(stack[1])
        if re.match('^[a-zA-Z].*',s0,0):
            s0 = str(hm.get(s0,s0))
        if re.match('^[a-zA-Z].*',s1,0):
            s1 = str(hm.get(s1,s1))
        if s0.isdigit and s1.isdigit:
            y = int(s0)
            x = int(s1)
            stack.pop(0)
            stack.pop(0)
            if x<y:
                return stack.insert(0, ':true:')
            else:
                return stack.insert(0, ':false:')
        else:
            return stack.insert(0, ':error:')
        
def doBind(stack, hm):
    if len(stack) < 2:
        return stack.insert(0,':error:')
    else:
        s0 = stack[0]
        s1 = stack[1]
        if re.match('^[a-zA-Z].*',stack[1],0) and stack[0] != ':error:':
            stack.pop(0)
            stack.pop(0)
            s0 = str(hm.get(s0,s0))
            hm[s1] = s0
            return stack.insert(0,':unit:')
        else:
            return stack.insert(0,':error:')

#hw4('input.txt', 'output.txt')
