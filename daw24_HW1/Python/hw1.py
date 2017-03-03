#################################################################
# Program reads in an input file(input.txt - a plain text file	#
# which contains 5 sentances), line by line anc check if the	#
# line read in is a pangram or not. If the sentence read is a	#
# pangram, it writes 'true' to the output file. If it's not, it #
# writes 'false' to the output file.				#
# Author: D. Weidenborner					#
# 1/12/2016							#
#################################################################

import string

# Checks letters from the alphabet against each sentance
def check(sent):
	letters = []
	for letter in sent:
		letters.append(letter)
	for letter in string.ascii_lowercase:
		if letter not in sent:
			return 0
	return 1

def hw1(input, output):
	# Read input file line by line
	f = open(input, 'r')
	strings = []
	for line in f:
		strings.append(line)
	f.close()
	
	# For every line in input file, check if it contains
	# all alphabets - store result (true/false) in a variable
	answers = []
	for line in strings:
		if (len(line) < 27):
			answers.append('false')
		elif (check(line) == 1):
			# Call helper function to check against alphabet
			answers.append('true')
		else:
			answers.append('false')
	
	# Write result to output file
	f = open(output, 'w')
	for i in answers:
		f.write(i)
		f.write('\n')
	f.close()

# For testing
#hw1('input.txt','output.txt')
