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
 * # 4/12/2016                                                             #
 * #########################################################################
 */
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
//import java.util.Scanner;
//import java.util.ArrayList;
import java.io.FileWriter;
import java.util.*;

public class hw3{
        public static void hw3(String inFile, String outFile)throws FileNotFoundException, IOException{
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
		Map binds = new HashMap();

		for(int i=0; i<lines.size(); i++){
			String[] exp = lines.get(i).split(" ");
			// Write the stack to a text file
			//System.out.println(exp[0]);
			if(exp[0].equals("quit")){
				//System.out.println("Printing to file");
				FileWriter out = new FileWriter(outFile);
				for(String item : stack){
					if(item.charAt(0) == '\"'){
						int len = item.length()-1;
						out.write(item.substring(1, len) + "\n");
					}
					else{
						out.write(item + "\n");
					}
				}
				out.close();
				return;
			}
			if(exp[0].equals("push")){
				push(stack, exp[1]);
			}
			else if(exp[0].equals("add")){
				add(stack, binds);			
			}
			else if(exp[0].equals("neg")){
				neg(stack, binds);
			}
			else if(exp[0].equals("mul")){
				mul(stack, binds);
			}
			else if(exp[0].equals("sub")){
				sub(stack, binds);
			}
			else if(exp[0].equals("div")){
				div(stack, binds);
			}
			else if(exp[0].equals("rem")){
				rem(stack, binds);
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
			else if(exp[0].equals(":error:")){
				error(stack);
			}
			else if(exp[0].equals("bind")){
				bind(stack, binds);
			}
			else if(exp[0].equals("and")){
				andMethod(stack, binds);
			}
			else if(exp[0].equals("or")){
				orMethod(stack, binds);
			}
			else if(exp[0].equals("not")){
				notMethod(stack, binds);
			}
			else if(exp[0].equals("equal")){
				equalMethod(stack, binds);
			}
			else if(exp[0].equals("lessThan")){
				lessThan(stack, binds);
			}
			else if(exp[0].equals("if")){
				ifMethod(stack, binds);
			}
			else if(exp[0].equals("let")){
				letMethod(stack);
			}
			else if(exp[0].equals("end")){
				endMethod(stack);
			}
		}
	}
	
	public static void push(ArrayList<String> inStack, String exp){
		if(exp.charAt(0) == '-'){
			if(exp.substring(1).matches("0")){
				inStack.add(0, "0");
			}
			else if(exp.substring(1).matches("[0-9]+")){
				inStack.add(0, exp);
			}
			else{
				error(inStack);
			}
		}
		else if(exp.matches("[0-9]+")){
			inStack.add(0, exp);
		}
		else if(exp.substring(0, 1).matches("[A-Za-z]")){
			inStack.add(0, exp);
		}
		else if(exp.charAt(0) == '\"'){
			inStack.add(0, exp);			
		}
		else{
			inStack.add(0, ":error:");
		}
		
	}
	
	public static boolean isNumInBinds(String exp, Map inBinds){
		if(inBinds.containsKey(exp)){
			String element = (String)inBinds.get(exp);
			if(isNum(element)) return true;
			else return false;
		}
		else return false;
	}

	public static void add(ArrayList<String> inStack, Map inBinds){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if ((isNum(inStack.get(0)) || isNumInBinds(inStack.get(0), inBinds)) &&
			 (isNum(inStack.get(1)) || isNumInBinds(inStack.get(1), inBinds))){
			String num1 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				num1 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			String num2 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				num2 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			int total = Integer.parseInt(num1) + Integer.parseInt(num2);
			inStack.add(0, Integer.toString(total));
		}
		else{
			error(inStack);
		}
	}
	
	public static void neg(ArrayList<String> inStack, Map inBinds){
		if(isNum(inStack.get(0)) || isNumInBinds(inStack.get(0), inBinds)){
			if(isNumInBinds(inStack.get(0), inBinds)){
				String varName = inStack.get(0);
				inStack.remove(0);
				int negNum = Integer.parseInt((String)inBinds.get(varName));
				negNum = 0 - negNum;
				inStack.add(0, Integer.toString(negNum));
			}
			else{
				int negNum = Integer.parseInt(inStack.get(0));
				inStack.remove(0);
				negNum = 0 - negNum;
				inStack.add(0, Integer.toString(negNum));
			}
		}
		else{
			error(inStack);
		}
	}

	public static void mul(ArrayList<String> inStack, Map inBinds){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if ((isNum(inStack.get(0)) || isNumInBinds(inStack.get(0), inBinds)) &&
			 (isNum(inStack.get(1)) || isNumInBinds(inStack.get(1), inBinds))){
			String num1 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				num1 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			String num2 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				num2 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			int total = Integer.parseInt(num1) * Integer.parseInt(num2);
			inStack.add(0, Integer.toString(total));
		}
		else{
			error(inStack);
		}
	}
	
	public static void sub(ArrayList<String> inStack, Map inBinds){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if ((isNum(inStack.get(0)) || isNumInBinds(inStack.get(0), inBinds)) &&
			 (isNum(inStack.get(1)) || isNumInBinds(inStack.get(1), inBinds))){
			String num1 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				num1 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			String num2 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				num2 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			int total = Integer.parseInt(num2) - Integer.parseInt(num1);
			inStack.add(0, Integer.toString(total));
		}
		else{
			error(inStack);
		}
	}
	
	public static void div(ArrayList<String> inStack, Map inBinds){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if ((isNum(inStack.get(0)) || isNumInBinds(inStack.get(0), inBinds)) &&
			 (isNum(inStack.get(1)) || isNumInBinds(inStack.get(1), inBinds))){
			
			String num1 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				num1 = (String)inBinds.get(inStack.get(0));
			}
			if(Integer.parseInt(num1) == 0) {
				error(inStack);
			}
			else{
				inStack.remove(0);
				String num2 = inStack.get(0);
				if (inBinds.containsKey(inStack.get(0))){
					num2 = (String)inBinds.get(inStack.get(0));
				}
				inStack.remove(0);
				int total = Integer.parseInt(num2) / Integer.parseInt(num1);
				inStack.add(0, Integer.toString(total));
			}
		}
		else{
			error(inStack);
		}
	}
	
	public static void rem(ArrayList<String> inStack, Map inBinds){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if ((isNum(inStack.get(0)) || isNumInBinds(inStack.get(0), inBinds)) &&
			 (isNum(inStack.get(1)) || isNumInBinds(inStack.get(1), inBinds))){
			
			String num1 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				num1 = (String)inBinds.get(inStack.get(0));
			}
			if(Integer.parseInt(num1) == 0) {
				error(inStack);
			}
			else{
				inStack.remove(0);
				String num2 = inStack.get(0);
				if (inBinds.containsKey(inStack.get(0))){
					num2 = (String)inBinds.get(inStack.get(0));
				}
				inStack.remove(0);
				int total = Integer.parseInt(num2) % Integer.parseInt(num1);
				inStack.add(0, Integer.toString(total));
			}
		}
		else{
			error(inStack);
		}
	}

	public static void equalMethod(ArrayList<String> inStack, Map inBinds){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if ((isNum(inStack.get(0)) || isNumInBinds(inStack.get(0), inBinds)) &&
			 (isNum(inStack.get(1)) || isNumInBinds(inStack.get(1), inBinds))){
			String num1 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				num1 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			String num2 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				num2 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			if(Integer.parseInt(num1) == Integer.parseInt(num2)){
				inStack.add(0, ":true:");
			}
			else{
				inStack.add(0, ":false:");
			}
		}
		else{
			error(inStack);
		}
	}

	public static void lessThan(ArrayList<String> inStack, Map inBinds){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if ((isNum(inStack.get(0)) || isNumInBinds(inStack.get(0), inBinds)) &&
			 (isNum(inStack.get(1)) || isNumInBinds(inStack.get(1), inBinds))){
			String num1 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				num1 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			String num2 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				num2 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			if(Integer.parseInt(num2) < Integer.parseInt(num1)){
				inStack.add(0, ":true:");
			}
			else{
				inStack.add(0, ":false:");
			}
		}
		else{
			error(inStack);
		}
	}

	public static boolean isBoolInBinds(String exp, Map inBinds){
		if(inBinds.containsKey(exp)){
			String element = (String)inBinds.get(exp);
			if(element.equals(":true:") || element.equals(":false:")) return true;
			else{
				//System.out.println("error value not boolean");
				return false;
			}
		}
		else{ 
			//System.out.println("error key doesnt exist");
			return false;
		}
	}

	public static void andMethod(ArrayList<String> inStack, Map inBinds){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if ((inStack.get(0).equals(":true:") || inStack.get(0).equals(":false:") || isBoolInBinds(inStack.get(0), inBinds)) &&
			 (inStack.get(1).equals(":true:") || inStack.get(1).equals(":false:") || isBoolInBinds(inStack.get(1), inBinds))){
			String bool1 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				bool1 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			String bool2 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				bool2 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			if(bool1.equals(":true:") && bool2.equals(":true:")){
				inStack.add(0, ":true:");
			}
			else{
				inStack.add(0, ":false:");
			}
		}
		else{
			error(inStack);
		}
	}

	public static void orMethod(ArrayList<String> inStack, Map inBinds){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if ((inStack.get(0).equals(":true:") || inStack.get(0).equals(":false:") || isBoolInBinds(inStack.get(0), inBinds)) &&
			 (inStack.get(1).equals(":true:") || inStack.get(1).equals(":false:") || isBoolInBinds(inStack.get(1), inBinds))){
			String bool1 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				bool1 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			String bool2 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				bool2 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			if(bool1.equals(":true:") || bool2.equals(":true:")){
				inStack.add(0, ":true:");
			}
			else{
				inStack.add(0, ":false:");
			}
		}
		else{
			error(inStack);
		}
	}

	public static void notMethod(ArrayList<String> inStack, Map inBinds){
		if (inStack.size() < 1){
			error(inStack);
		}
		else if(inStack.get(0).equals(":true:") || inStack.get(0).equals(":false:") || isBoolInBinds(inStack.get(0), inBinds)){
			String bool1 = inStack.get(0);
			if (inBinds.containsKey(inStack.get(0))){
				bool1 = (String)inBinds.get(inStack.get(0));
			}
			inStack.remove(0);
			if(bool1.equals(":true:")){
				inStack.add(0, ":false:");
			}
			else{
				inStack.add(0, ":true:");
			}
		}
		else{
			error(inStack);
		}
	}

	public static void ifMethod(ArrayList<String> inStack, Map inBinds){
		if (inStack.size() < 3){
			error(inStack);
		}
		else if(inStack.get(2).equals(":true:") || inStack.get(2).equals(":false:") || isBoolInBinds(inStack.get(2), inBinds)){
			String bool1 = inStack.get(2);
			if (inBinds.containsKey(inStack.get(2))){
				bool1 = (String)inBinds.get(inStack.get(2));
			}
			inStack.remove(2);
			if(bool1.equals(":true:")){
				inStack.remove(1);
			}
			else{
				inStack.remove(0);
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

	public static void bind(ArrayList<String> inStack, Map inBinds){
		if (inStack.size() < 2){
			error(inStack);
		}
		else if (!Character.isLetter((inStack.get(1)).charAt(0)) || inStack.get(0).equals(":error:")){
			error(inStack);
		}
		//else if(inStack.get(0).equals(":error:")) { 
		//	error(inStack);
		//}
		else{
			String var = inStack.get(0);
			inStack.remove(0);
			String varName = inStack.get(0);
 			inStack.remove(0);
			if (inBinds.containsKey(var)){
				inBinds.put(varName, inBinds.get(var));
			}
			else{
				inBinds.put(varName, var);
			}
			inStack.add(0, ":unit:");
		}
	}

	public static void letMethod(ArrayList<String> inStack){
		inStack.add(0, "\"let");
	}

	public static void endMethod(ArrayList<String> inStack){
		int index = inStack.indexOf("\"let");
		while(index > 0){
			inStack.remove(index);
			index--;	
		}
	}
}

