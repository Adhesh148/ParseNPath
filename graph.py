from collections import defaultdict

# Define Graph class
class Graph:



	# Define init
	def __init__(self, num_vertices,nodes,fp):

		# Store number of vertices
		self.N = num_vertices
		self.nodes = nodes

		# Define the adjacency list
		self.adjList = defaultdict(list)

		# Set file pointer value
		self.fp = fp

	# Define Add Edge Function
	def addEdge(self, u, v):
		self.adjList[u].append(v)

	# Define the Utitlity function to print all paths from source to dest
	def printAllPathsUtil(self, u, v, isVisited, path):

		# Mark u as visited and store in path
		isVisited[u] = 1
		path.append(self.nodes[u])

		if(u == v):
			line = '-> '.join(path)
			if(self.fp != -1):
				self.fp.write(line+"\n")
			print(*path, sep=' -> ')
		else:
			# Recursively visit all nodes not visited that are adjacent to u
			for i in self.adjList[u]:
				if(isVisited[i] == 0):
					self.printAllPathsUtil(i,v,isVisited,path)

		# If destination is unreachable from current node, delete it from path
		path.pop()
		isVisited[u] = 0

	# Define the starter function for printAllPaths
	def printAllPaths(self, source, destination):

		# Clear isVisited list
		isVisited = [0] * self.N

		# Initiate an empty path list
		path = []

		# Call the Util Function
		self.printAllPathsUtil(source, destination, isVisited, path)