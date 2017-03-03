/*
#################################################################
# Program reads in an input file(input.txt - a plain text file  #
# which contains 5 sentances), line by line anc check if the    #
# line read in is a pangram or not. If the sentence read is a   #
# pangram, it writes 'true' to the output file. If it's not, it #
# writes 'false' to the output file.                            #
# Author: D. Weidenborner                                       #
# 1/15/2016                                                     #
#################################################################
*/

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;
import java.util.ArrayList;
import java.io.FileWriter;

public class hw1{
	public static void hw1(String inFile, String outFile)throws FileNotFoundException, IOException{
		//Function defined here
		ArrayList<String> lines = new ArrayList<String>();
		File inputFile = new File(inFile);
		Scanner in = new Scanner(inputFile);
		while (in.hasNextLine()){ 
			String line = in.nextLine();
			lines.add(line);
		}
		in.close()
;
		ArrayList<String> letters = new ArrayList<String>();
		ArrayList<String> answers = new ArrayList<String>();
		// For each string
		for(int i = 0; i < lines.size(); i++){
			// Flag to check if a letter was not found
			// Set to 1 when letter not found so value is not set to true
			int flag = 0;
			// For each letter a-z lowercase
			for(char letter = 'a'; letter <= 'z'; letter++){
				int num = lines.get(i).indexOf(letter);
				// Returns -1 if letter not found
				if(num < 0){
					answers.add("false");
					flag = 1;
					break;
				}
			}
			// If flag is still zero after itterating through string it is a pangram
			if(flag == 0){
				answers.add("true");
			}
			// If flag was raised then answer was already set to false
			// Reset flag and continue to next string
			else if(flag == 1){
				flag = 0;
			}	
		}
		FileWriter out = new FileWriter(outFile);				
		for(String answer : answers){
			out.write(answer + "\n");
		}
		out.close();
	}
}
