import sys
import re
sys.path.append(".")
from graph import Graph

KEYWORDS = ['input','output','wire']
GATES = ['nand','and', 'or', 'not', 'xor', 'nor', 'xnor']
DEMILITERS = [",",";","(",")"]
module_name = ""

def parser(input_file,input_nodes,output_nodes,wires):

	# Open input_file
	fo = open(input_file,"r")

	# Define variables
	connections = []
	conn_indx = 0

	# read the file line by line and process
	while(1):
		
		line = fo.readline()
		tokens = line.strip().split(" ")

		# Check if comments
		if(tokens[0] == "//"):
			continue

		# Check if multi-line comments
		if(tokens[0] == "/*"):
			while(fo.readline().strip().split(" ")[0] != "*/"):
				continue

		# Check for endmodule
		if(tokens[0] == "endmodule"):
			break

		# Get module name and implicit decalaration
		if(tokens[0] == "module"):

			# Find module name
			x = re.findall(r"module[\s]+[\w*]+\b",line)
			if(len(x) != 0):
				s = re.sub(' +',' ',x[0])
				global module_name
				module_name = s.split(" ")[1]

			x = re.findall(r"\)",line);
			while(len(x)==0):
				# Check for inputs
				x = re.findall(r"input[\s]+[\w*]+\b",line)
				for i in x:
					s = re.sub(' +',' ',i)
					input_nodes.append(s.split(" ")[1])

				# Check for outputs
				x = re.findall(r"output[\s]+[\w*]+\b",line)
				for i in x:
					s = re.sub(' +',' ',i)
					output_nodes.append(s.split(" ")[1])

				# Check for input vector
				x = re.findall(r"input[\s]+\[(?:.*?)\][\s]+\w*\b",line)
				for i in x:
					s = re.sub(' +',' ',i)
					vector_range = re.findall(r"\d+[\s]*:[\s]*\d+",s)
					vector_range = vector_range[0].split(":")
					start_indx = int(vector_range[0])
					end_indx = int(vector_range[1])
					s = s.split(" ")
					# Append each individual vector into the input nodes list
					if(start_indx > end_indx):
						start_indx, end_indx = end_indx, start_indx
					for indx in range(start_indx, end_indx):
						node = ""+s[-1]+"["+str(indx)+"]"
						input_nodes.append(node)
					
				# Check for output vector
				x = re.findall(r"output[\s]+\[(?:.*?)\][\s]+\w*\b",line)
				for i in x:
					s = re.sub(' +',' ',i)
					vector_range = re.findall(r"\d+[\s]*:[\s]*\d+",s)
					vector_range = vector_range[0].split(":")
					start_indx = int(vector_range[0])
					end_indx = int(vector_range[1])
					s = s.split(" ")
					# Append each individual vector into the input nodes list
					if(start_indx > end_indx):
						start_indx, end_indx = end_indx, start_indx
					for indx in range(start_indx, end_indx):
						node = ""+s[-1]+"["+str(indx)+"]"
						output_nodes.append(node)

				line = fo.readline()
				x = re.findall(r"\)",line);
			continue

		# Get input/output from IO Port Declarations (Case: When it is not implicit declarations)
		if(tokens[0] in KEYWORDS):
			# Get Inputs
			x = re.findall(r"input[\s]+(?!\[)[^;]*",line)
			if(len(x)!=0):
				while(";" not in line):
					line = line + fo.readline()
				x = re.findall(r"input[\s]+(?!\[)[^;]*",line)
				s = re.sub(' +',' ',x[0])
				s = s.split(",")
				node = s[0].split(" ")[1]
				input_nodes.append(node)
				for i in range(1,len(s)):
					input_nodes.append(s[i].strip())

			# Get Outputs
			x = re.findall(r"output[\s]+(?!\[)[^;]*",line)
			if(len(x)!=0):
				while(";" not in line):
					line = line + fo.readline()
				x = re.findall(r"output[\s]+(?!\[)[^;]*",line)
				s = re.sub(' +',' ',x[0])
				s = s.split(",")
				node = s[0].split(" ")[1]
				output_nodes.append(node)
				for i in range(1,len(s)):
					output_nodes.append(s[i].strip())

			# Get Wires
			x = re.findall(r"wire[\s]+(?!\[)[^;]*",line)
			if(len(x)!=0):
				while(";" not in line):
					line = line + fo.readline()
				x = re.findall(r"wire[\s]+(?!\[)[^;]*",line)
				s = re.sub(' +',' ',x[0])
				s = s.split(",")
				node = s[0].split(" ")[1]
				wires.append(node)
				for i in range(1,len(s)):
					wires.append(s[i].strip())

			# Get input vectors
			x = re.findall(r"input[\s]+\[(?:.*?)\][\s]+\w*[^;]*",line)
			if(len(x)!=0):
				s = re.sub(' +',' ',x[0])
				vector_range = re.findall(r"\d+[\s]*:[\s]*\d+",s)
				vector_range = vector_range[0].split(":")
				start_indx = int(vector_range[0])
				end_indx = int(vector_range[1])
				if(start_indx > end_indx):
					start_indx, end_indx = end_indx, start_indx
				while(";" not in line):
					line = line + fo.readline()
				x = re.findall(r"\][^;]*",line)
				s = re.sub(' +',' ',x[0])
				s = s[1:]
				s = s.split(",")
				for i in s:
					for indx in range(start_indx, end_indx):
						node = ""+i.strip()+"["+str(indx)+"]"
						input_nodes.append(node)

			# Get output vectors
			x = re.findall(r"output[\s]+\[(?:.*?)\][\s]+\w*[^;]*",line)
			if(len(x)!=0):
				s = re.sub(' +',' ',x[0])
				vector_range = re.findall(r"\d+[\s]*:[\s]*\d+",s)
				vector_range = vector_range[0].split(":")
				start_indx = int(vector_range[0])
				end_indx = int(vector_range[1])
				if(start_indx > end_indx):
					start_indx, end_indx = end_indx, start_indx
				while(";" not in line):
					line = line + fo.readline()
				x = re.findall(r"\][^;]*",line)
				s = re.sub(' +',' ',x[0])
				s = s[1:]
				s = s.split(",")
				for i in s:
					for indx in range(start_indx, end_indx):
						node = ""+i.strip()+"["+str(indx)+"]"
						output_nodes.append(node)

			# Get wire vectors
			x = re.findall(r"wire[\s]+\[(?:.*?)\][\s]+\w*[^;]*",line)
			if(len(x)!=0):
				s = re.sub(' +',' ',x[0])
				vector_range = re.findall(r"\d+[\s]*:[\s]*\d+",s)
				vector_range = vector_range[0].split(":")
				start_indx = int(vector_range[0])
				end_indx = int(vector_range[1])
				if(start_indx > end_indx):
					start_indx, end_indx = end_indx, start_indx
				while(";" not in line):
					line = line + fo.readline()
				x = re.findall(r"\][^;]*",line)
				s = re.sub(' +',' ',x[0])
				s = s[1:]
				s = s.split(",")
				for i in s:
					for indx in range(start_indx, end_indx):
						node = ""+i.strip()+"["+str(indx)+"]"
						wires.append(node)
			continue

		# Get connection details from gate instantiation
		if(tokens[0] in GATES):
			start_indx = 1
			# Check for nameless instantition
			if(tokens[1][0] != "("):
				start_indx = start_indx + 1

			node = ""
			connections.append([])
			for i in range(start_indx,len(tokens)):
				for j in range(0,len(tokens[i])):
					if(tokens[i][j] not in DEMILITERS):
						node += tokens[i][j]
					else:
						if(len(node) > 0):
							connections[conn_indx].append(node)
						node = ""
			conn_indx += 1

		# Line Termination condition
		if not line:
			break

	return connections


def createGraph(module_name,connections,input_nodes,output_nodes, wires, fp):

	# Instanatiate the graph
	num_vertices = len(input_nodes) + len(output_nodes) + len(wires)
	nodes = input_nodes + output_nodes + wires
	g = Graph(num_vertices,nodes,fp)

	# Print initial details
	if(fp!=-1):
		pattern = "="*210
		fp.write(pattern+"\n")
		fp.write("Module Name: "+module_name+"\n")
		fp.write("Input Nodes: "+str(input_nodes)+"\n")
		fp.write("Output Nodes: "+str(output_nodes)+"\n")
		fp.write("Wires: "+str(wires)+"\n")
		fp.write(pattern+"\n\n")

	# Build the graph
	for conn in connections:
		out = nodes.index(conn[0])
		for indx in range(1,len(conn)):
			g.addEdge(nodes.index(conn[indx]),out)

	# Enumerate all paths from all inputs to outputs
	for curr_input in input_nodes:
		for curr_output in output_nodes:
			line = "Path(s) from "+curr_input+" to "+curr_output+":\n"
			if(fp!=-1):
				fp.write(line)
			print (line) 
			g.printAllPaths(nodes.index(curr_input),nodes.index(curr_output))
			if(fp!=-1):
				fp.write("\n")
			print("\n",end="")


def main():	

	# Print welcome message
	print("###############################################################################################")
	print("#                                                                                             #")
	print("#                 Welcome to Gate-Level Parser and Path Finder Program                        #")
	print("#                 Author: Adhesh Reghu Kumar (COE18B001)  IIITDM                              #")
	print("#                                                                                             #")
	print("#  Instructions to Use: Enter the input verilog file name. eg: sample.v                       #")
	print("#                                                                                             #")
	print("#  Note: This program doesnt not check the correctness of the verilog file.                   #")
	print("#        It assumes the file is syntatically correct.                                         #")
	print("#                                                                                             #")
	print("#  The program currently supports simple gate level design based codes.                       #")
	print("#  It supports inputs, outputs, wires and 1D vectors.                                         #")
	print("#                                                                                             #")
	print("###############################################################################################")

	print("\nEnter input file name.")
	input_file = input().strip()

	# Define Variables
	input_nodes = []
	output_nodes = []
	wires = []
	
	print("\n[PARSER] Input file is being parsed ...")
	connections = parser(input_file, input_nodes, output_nodes, wires)
	print("\n[PARSER] Module Name:",module_name)
	print("\n[PARSER] Input Nodes:",input_nodes)
	print("\n[PARSER] Output Nodes:",output_nodes)
	print("\n[PARSER] Wires:",wires)
	print("\n[PARSER] Connection details:\n",connections,"\n")

	# Write to File Option
	outfile = ""
	fp = -1
	print("Do you wish to write the path details to an output file (Y/N).")
	response = input().strip()
	if(response == "Y"):
		print("Enter name of the output file.")
		outfile = input().strip()
		fp = open(outfile,"w")

	# Create graph from the connections details derived from parser
	g = createGraph(module_name, connections, input_nodes, output_nodes, wires, fp)


if __name__ == '__main__':
	main()