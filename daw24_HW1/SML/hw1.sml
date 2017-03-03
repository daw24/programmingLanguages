(*###############################################################
# Program reads in an input file(input.txt - a plain text file  #
# which contains 5 sentances), line by line anc check if the    #
# line read in is a pangram or not. If the sentence read is a   #
# pangram, it writes 'true' to the output file. If it's not, it #
# writes 'false' to the output file.                            #
# Author: D. Weidenborner                                       #
# 1/17/2016                                                     #
###############################################################*)

fun hw1(inFile : string, outFile: string) =
let
	
	(* Open input and output file streams, read first input line from
   	   the input file stream *)
	val inStream = TextIO.openIn inFile
	val outStream = TextIO.openOut outFile
	val readLine = TextIO.inputLine inStream
	(* Convert the string type of the lines read and alphabet string to list type*)
	val alphabet = explode("abcdefghijklmnopqrstuvwxyz")

	fun checkLetter(a,b) = List.exists(fn y => y = b) a	

(*	(* Tried itterating through alphabet, but I was gettting errors for i::j, and
	   operand operator mismatch errors which j somehow being type char list. 
	   I could not figure it out so I cheesed it and called my checkLetter function
	   for each letter. *)

	fun checkLine (a, b) = 
		case b of
		[] => true
		| (a, i::j) =>  if  checkLetter(explode(a), i) then checkLetter(explode(a), j)
			else false
*)

	(* Perform alphabet checks on these lists *)
	fun checkLine (a) = if  checkLetter(explode(a), #"a") andalso 
				checkLetter(explode(a), #"b") andalso 
				checkLetter(explode(a), #"c") andalso
				checkLetter(explode(a), #"d") andalso 
				checkLetter(explode(a), #"e") andalso 
				checkLetter(explode(a), #"f") andalso 
				checkLetter(explode(a), #"g") andalso 
				checkLetter(explode(a), #"h") andalso 
				checkLetter(explode(a), #"i") andalso 
				checkLetter(explode(a), #"j") andalso 
				checkLetter(explode(a), #"k") andalso 
				checkLetter(explode(a), #"l") andalso 
				checkLetter(explode(a), #"m") andalso 
				checkLetter(explode(a), #"n") andalso 
				checkLetter(explode(a), #"o") andalso 
				checkLetter(explode(a), #"p") andalso
				checkLetter(explode(a), #"q") andalso
				checkLetter(explode(a), #"r") andalso
				checkLetter(explode(a), #"s") andalso
				checkLetter(explode(a), #"t") andalso
				checkLetter(explode(a), #"u") andalso
				checkLetter(explode(a), #"v") andalso
				checkLetter(explode(a), #"w") andalso
				checkLetter(explode(a), #"x") andalso
				checkLetter(explode(a), #"y") andalso
				checkLetter(explode(a), #"z") then "true\n" else "false\n";
		
	(* To read subsequent lines, you can make use of a helper function *)
	fun nextLine(readLine : string option) =
		case readLine of
			    NONE => (TextIO.closeIn inStream; TextIO.closeOut outStream)
			(*Write the resultant value – true or false to the output file *)
			| SOME(c) => (TextIO.output(outStream, checkLine(c));
				      (nextLine(TextIO.inputLine inStream)))
in
	nextLine(readLine)
end;



(* This last line is the function call to hw1 to test your code. Don’t include this in your
submission but use this line to test your code

val _ = hw1("input.txt", "output.txt") *) 
