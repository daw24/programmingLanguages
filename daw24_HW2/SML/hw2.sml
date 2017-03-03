(*#######################################################################
# The goal of this homework is to understand and build an interpreter   #
# in three languages (Python, SML, Java, 20 marks for each) for a small #
# language. Your interpreter should read in an input file (input.txt)   #
# which contains lines of expressions, evaluate them and push the       #
# results onto a stack, then print the content of the stack to an       #
# output file (output.txt) when exit. This homework is the first of a   #
# multi-part homework, you will be implementing some of the features.   #
# More interesting features will be introduced in the following         #
# homework.                                                             #
# Author: D. Weidenborner                                               #
# 3/6/2016                                                             #
#######################################################################*)

fun printElem([]) = ()
	| printElem(a::b) = (print(a ^ "\n"); printElem(b));

fun push(x, inStack) = 
	if x = "-0\n" then "0\n"::inStack (*not working for some reason*) 
	else x::inStack 

exception stackError

fun pop(x::xs) = "pop\n"::xs
	|pop([]) = push(":error:\n", [])

fun sendTrue(inStack) =
	inStack @ [":true:\n"]

fun sendFalse(inStack) =
	inStack @ [":false:\n"]

(*fun add(x::xs) =
	String.toInt(x) + String.toInt(hd(xs)) *)

fun reverse([]) = []
	|reverse(x::xs) = reverse(xs) @ [x]

fun checkCmd([], inStack) = []
	|checkCmd(x::xs, inStack) =
	if x = "push" then (*(print("equals, cmd is " ^ x ^ "\n");*) push(hd(xs), inStack)
	else if x = "pop\n" then pop(inStack)
	else if x = ":true:\n" then sendTrue(inStack)
	else if x = ":false:\n" then sendFalse(inStack)
	else checkCmd(xs, inStack)

fun outputString([]) = "" 
	|outputString(x::xs) =  x^(outputString(xs))

fun combine([], []) = []
	|combine(list1, list2) = list1 @ list2

fun hw2(inFile : string, outFile : string) = 
	let
		val stack = []
		val outStack = []
		val inStream = TextIO.openIn inFile
		val outStream = TextIO.openOut outFile
		val readLine = TextIO.inputLine inStream
	 	fun checkExp(exp : string option) =
			let
				val expression = getOpt(exp," ")
				(*val _ = print(expression)*)
				val expParts = (String.tokens (fn c => c = #" "))
				(*val _ = print("expParts: \n")
				val _ = printElem(expParts(expression))*)
				val newStack = checkCmd(expParts(expression), stack)
				val _ = combine(newStack, outStack) 
				(*val _ = printElem(newStack)*)
				val _ = TextIO.output(outStream, outputString(newStack))
				val _ = TextIO.flushOut(outStream)
			in
				true
			end
		
		(*val _ = printElem(outStack)
		val _ = TextIO.output(outStream, outputString(outStack))
		val _ = TextIO.flushOut(outStream)*)

		fun nextLine(readLine : string option) =
			case readLine of
				NONE => (TextIO.closeIn inStream; TextIO.closeOut outStream)
			| SOME(c) => (checkExp( readLine);
				      nextLine(TextIO.inputLine inStream))
	in
		nextLine(readLine)
	end

(*val _ = hw2("input.txt", "output.txt")*)
