'''kruskal.py: Graph Theory/Greedy Algorithm'''

'''@author: Pranjal Verma'''

'''dicts in python 3.6:
	https://stackoverflow.com/questions/39980323/dictionaries-are-ordered-in-python-3-6

	using OrderedDict in this code as proposition in link^ is a CPython implementation detail
	and should not be relied upon.
'''

'''sorting by costs:
	generic sorting algorithm in 'sorted()' is O(mlogm), where m is num of edges that are being 
	sorted, but we know that m = O(n^2) for a connected graph with no parallel edges, 
	so O(mlogm) = O(mlogn)!
	Even if there's parallel edges, we'll just remove them in O(m) time in a preprocessing step
	to only keep the edge with min cost from among these parallel edges.
'''

'''main for-loop in optimised kruskal's (Amortized analysis; google):
	overall running time for this loop is O(nlogn) because any node in the graph will change
	it's parent O(logn) times overall because parent changes only happen when two sets merge 
	and one set is at least twice as big as the other. Thus for n nodes, num of parent pointers
	changed is O(nlogn), each pointer change taking O(1) time.
	Main for-loop will run till exactly O(nlogn) pointer changes have been made and only one set
	containing all nodes of graph remains, at which point the 'break' condition is triggered.
	Since this 'union' operation is the only time-significant process in this loop, 
	entire loop's runtime is O(nlogn)! QED, mate!
'''

'''This code also contains my naïve implementaion of the UnionFind data structure for 
disjoint sets'''

from collections import OrderedDict, defaultdict
from operator import itemgetter
from time import time

#eager union-find data structure for optimised kruskal's
#raison d'être: maintaining partitions of a set of objects
#can be optimised using union by rank and path compression for lazy unions
class UnionFind():

	#init with the partition sets and a parent table
	#can be optimised using only 'parents' dict
	def __init__(self):
		self.sets = defaultdict(list)
		self.parents = defaultdict(int)

	#insert object in a set; here node is inserted in it's own, lonely set
	def insert(self, node):
		if node not in self.parents:
			self.sets[node].append(node)
			self.parents[node] = node

	#finding parents of nodes in given edge
	def find(self, edge):
		return self.parents[edge[0]], self.parents[edge[1]]

	#merging two disjoint connected components of graph
	def union(self, parent1, parent2):

		#discarding parent of smaller set to minimise pointer changes
		if len(self.sets[parent1]) > len(self.sets[parent2]):
			self.sets[parent1].extend(self.sets[parent2]) #O(k)
			for v in self.sets[parent2]:
				self.parents[v] = parent1

			del self.sets[parent2]
		else:
			self.sets[parent2].extend(self.sets[parent1]) #O(k)
			for v in self.sets[parent1]:
				self.parents[v] = parent2

			del self.sets[parent1]

#optimised kruskal's, using the UnionFind DS to check for cycles inside the main for-loop
#Run-time: O(mlogn)
def kruskal(graph):

	#sorting given graph in order of increasing edge costs; O(mlogn), explaination above^
	#read link above^ for dict() uses
	sortedGraph = OrderedDict(sorted(graph.items(), key=itemgetter(0)))
	tree, treeCost = defaultdict(list), 0

	#inserting all nodes of graph in the UnionFind object; O(m)
	#CC = connected components
	CCs = UnionFind()
	for cost in sortedGraph:
		for edge in sortedGraph[cost]:
			CCs.insert(edge[0])
			CCs.insert(edge[1])

	#iterating over sorted costs; main for-loop; O(nlogn)
	#run-time of this loop is explained above^
	for cost in sortedGraph:

		#if 'tree' becomes connected, we can stop exploring further edges
		if len(tree) == numNodes:
			break

		#looping over edges with same cost; max num of edges with same cost = 4 in given graph
		#this loop runs at max 4 times for given graph
		for edge in sortedGraph[cost]:

			#checking if both nodes of edge belong to same connected component or not
			#if they do, adding them creates a cycle so this edge is not added to MST
			u, v = CCs.find(edge)
			if u != v:

				#constructing MST, while maintaining UnionFind invariant:

				tree[edge[0]].append(edge[1])
				tree[edge[1]].append(edge[0])
				treeCost += cost
				CCs.union(u, v)

	return treeCost

#naïve kruskal's, using O(n) bfs routine to check for cycles inside the main for-loop
#Run-time: O(mn)
def badKruskal(graph):

	#similar sorting and dict() uses as optimised kruskal's
	sortedGraph = OrderedDict(sorted(graph.items(), key=itemgetter(0)))
	tree, treeCost = defaultdict(list), 0

	#main for-loop uses a bfs routine to check for cycles
	for cost in sortedGraph:	
		if len(tree) == numNodes:
			break

		#taking care of multiple edges with same cost, O(4)*O(n) = O(n)
		for edge in sortedGraph[cost]:

			#bfs for checking cycles; O(n)
			if not hasPath(tree, edge):

				#constructing MST:

				tree[edge[0]].append(edge[1])
				tree[edge[1]].append(edge[0])
				treeCost += cost

	return treeCost

#bfs routine for checking cycles in naïve kruskal's;
#which is reduced to checking if there's path from u to v for edge (u, v); O(n)
def hasPath(graph, edge):

	#if u or v not in tree, no path exists b/w them, thus edge (u, v) can be added to MST
	start, end = edge[0], edge[1]
	if start not in graph or end not in graph:
		return False

	#init
	explored = [False] * 500
	queue, explored[-1 * start] = [start], True

	#loop until queue is empty
	while queue:
		v = queue.pop(0)
		for w in graph[v]:
			if not explored[-1 * w]:
				explored[-1 * w] = True
				queue.append(w)

	return explored[-1 * edge[1]]

#init		
if __name__ == '__main__':
	draft, graph = open('undirectedGraph (weighted, 500).txt').read().splitlines(), defaultdict(list)
	numNodes = 500

	for line in draft[1:]:
		edge = list(map(int, line.split()))
		graph[edge[2]].append(tuple(edge[:2]))

	startTime = time()
	print('Bad kruskal: ' + str(badKruskal(graph)) + ', Time: ' + str(time() - startTime))

	startTime = time()
	print('Good kruskal: ' + str(kruskal(graph)) + ', Time: ' + str(time() - startTime))
