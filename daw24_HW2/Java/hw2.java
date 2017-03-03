/*
 * #########################################################################
 * # The goal of this homework is to understand and build an interpreter   #
 * # in three languages (Python, SML, Java, 20 marks for each) for a small #
 * # language. Your interpreter should read in an input file (input.txt)   #
 * # which contains lines of expressions, evaluate them and push the       #
 * # results onto a stack, then print the content of the stack to an       #
 * # output file (output.txt) when exit. This homework is the first of a   #
 * # multi-part homework, you will be implementing some of the features.   #
 * # More interesting features will be introduced in the following         #
 * # homework.                                                             #
 * # Author: D. Weidenborner                                               #
 * # 3/3/2016                                                             #
 * #########################################################################
 */
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;
import java.util.ArrayList;
import java.io.FileWriter;

public class hw2{
        public static void hw2(String inFile, String outFile)throws FileNotFoundException, IOException{
                // Read in the input text 
                ArrayList<String> lines = new ArrayList<String>();
                File inputFile = new File(inFile);
                Scanner in = new Scanner(inputFile);
                while (in.hasNextLine()){
                        String line = in.nextLine();
                        lines.add(line);
                }
                in.close();

		ArrayList<String> stack = new ArrayList<String>();

		for(int i=0; i<lines.size(); i++){
			String[] exp = lines.get(i).split(" ");
			// Write the stack to a text file
			//System.out.println(exp[0]);
			if(exp[0].equals("quit")){
				//System.out.println("Printing to file");
				FileWriter out = new FileWriter(outFile);
				for(String item : stack){
					out.write(item + "\n");
				}
				out.close();
				return;
			}
			if(exp[0].equals("push")){
				push(stack, exp[1]);
			}
			else if(exp[0].equals("add")){
				add(stack);			
			}
			else if(exp[0].equals("neg")){
				neg(stack);
			}
			else if(exp[0].equals("mul")){
				mul(stack);
			}
			else if(exp[0].equals("sub")){
				sub(stack);
			}
			else if(exp[0].equals("div")){
				div(stack);
			}
			else if(exp[0].equals("rem")){
				rem(stack);
			}
			else if(exp[0].equals(":true:")){
				stack.add(0, exp[0]);
			}
			else if(exp[0].equals(":false:")){
				stack.add(0, exp[0]);
			}
			else if(exp[0].equals("pop")){
				pop(stack);
			}
			else if(exp[0].equals("swap")){
				swap(stack);
			}
		}
	}
	
	public static void push(ArrayList<String> inStack, String exp){
		if(Integer.parseInt(exp) == 0){
			inStack.add(0, "0");
		}
		else{
			inStack.add(0, exp);
		}
	}
	
	public static void add(ArrayList<String> inStack){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if (isNum(inStack.get(0)) && isNum(inStack.get(1))){
			String num1 = inStack.get(0);
			inStack.remove(0);
			String num2 = inStack.get(0);
			inStack.remove(0);
			int total = Integer.parseInt(num1) + Integer.parseInt(num2);
			inStack.add(0, Integer.toString(total));
		}
		else{
			error(inStack);
		}
	}
	
	public static void neg(ArrayList<String> inStack){
		if(isNum(inStack.get(0))){
			int negNum = Integer.parseInt(inStack.get(0));
			inStack.remove(0);
			negNum = 0 - negNum;
			inStack.add(0, Integer.toString(negNum));
		}
		else{
			error(inStack);
		}
	}

	public static void mul(ArrayList<String> inStack){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if (isNum(inStack.get(0)) && isNum(inStack.get(1))){
			String num1 = inStack.get(0);
			inStack.remove(0);
			String num2 = inStack.get(0);
			inStack.remove(0);
			int total = Integer.parseInt(num1) * Integer.parseInt(num2);
			inStack.add(0, Integer.toString(total));
		}
		else{
			error(inStack);
		}
	}
	
	public static void sub(ArrayList<String> inStack){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if (isNum(inStack.get(0)) && isNum(inStack.get(1))){
			String num1 = inStack.get(0);
			inStack.remove(0);
			String num2 = inStack.get(0);
			inStack.remove(0);
			int total = Integer.parseInt(num2) - Integer.parseInt(num1);
			inStack.add(0, Integer.toString(total));
		}
		else{
			error(inStack);
		}
	}
	
	public static void div(ArrayList<String> inStack){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if (isNum(inStack.get(0)) && isNum(inStack.get(1))){
			if (Integer.parseInt(inStack.get(0)) == 0){
				error(inStack);
			}
			else{
				String num1 = inStack.get(0);
				inStack.remove(0);
				String num2 = inStack.get(0);
				inStack.remove(0);
				int total = Integer.parseInt(num2) / Integer.parseInt(num1);
				inStack.add(0, Integer.toString(total));
			}
		}
		else{
			error(inStack);
		}
	}
	
	public static void rem(ArrayList<String> inStack){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if (isNum(inStack.get(0)) && isNum(inStack.get(1))){
			if (Integer.parseInt(inStack.get(0)) == 0){
				error(inStack);
			}
			else{
				String num1 = inStack.get(0);
				inStack.remove(0);
				String num2 = inStack.get(0);
				inStack.remove(0);
				int total = Integer.parseInt(num2) % Integer.parseInt(num1);
				inStack.add(0, Integer.toString(total));
			}
		}
		else{
			error(inStack);
		}
	}

	public static void pop(ArrayList<String> inStack){
		if(inStack.size() < 1){
			error(inStack);
		}
		else{
			inStack.remove(0);
		}
	}
	
	public static void swap(ArrayList<String> inStack){
		if(inStack.size() < 2){
			error(inStack);
		}
		else{
			inStack.add(0, inStack.get(1));
			inStack.remove(2);
		}
	}
	
	public static boolean isNum(String str){
		return str.matches("-?\\d+?");
	}
	
	public static void error(ArrayList<String> inStack){
		inStack.add(0, ":error:");
	}

}





