'''tsp.py: NP-Complete/Dynamic Programming'''

'''@author: Pranjal Verma'''

'''
	TSP vs MST:
	https://stackoverflow.com/questions/3838747/can-tsp-be-solved-by-finding-minimum-spanning-tree-for-the-graph

	"If you're having trouble seeing the difference, in MST, you need to find a minimum weight 
	tree in a weighted graph, while in TSP you need to find a minimum weight path 
	(or cycle / circuit)."
'''

'''
	The Hamiltonian path problem:
	Given an undirected graph with n vertices, decide whether or not there is a (cycle-free) 
	path with n−1 edges that visits every vertex exactly once
'''

from itertools import combinations
from math import inf, sqrt
from time import process_time
import numpy as np

#sub-optimal O((n^2)*2^n) time TSP algorithm
def tsp(cities):

	#init: using numpy zeros for better memory management!
	#creating a dict to index different sets
	cache, i, setDict = np.zeros((len(cities), 2**len(cities))), 1, {}

	#init for source node 1, wrt to all combination sets, O(2^n)
	for r in cities:
		for nodeSet in list(map(list, combinations(cities, r))):

			#defining index for nodeSet
			setDict[tuple(nodeSet)] = i
			i += 1

			#if set only has one, it's path has value 0
			if nodeSet == [1]:
				cache[-1 * 1][-1 * i] = 0

			#getting from 1 to 1 while including any other num of nodes violates TSP
			#thus their value is inf
			else:
				cache[-1 * 1][-1 * i] = inf

			print('Running...')

	#for all 2^n combination sets, considering only those sets with source 1 in them, O(2^n)
	for size in list(cities)[1:]:
		for nodeSet in list(map(list, combinations(cities, size))):
			if 1 in nodeSet:

				#for all other j nodes in this set, apart from 1 itself, O(n)
				for nodej in nodeSet:
					if nodej != 1:

						#remove node j from this set, O(n)
						nodes = list(nodeSet)
						nodes.remove(nodej)

						#solve recurrence for this node and set, O(n)
						cache[-1 * nodej][-1 * setDict[tuple(nodeSet)]] = min(cache[-1 * nodek][-1 * setDict[tuple(nodes)]] + distance(nodek, nodej)
															for nodek in nodeSet
															if nodek != nodej)

			print('Running...')

	#finally complete cycle considering all choices and return the best cycle, O(n)
	return min(cache[-1 * j][-1 * setDict[tuple(cities)]] + distance(j, 1) for j in range(2, len(cities) + 1))

#func to compute euclidean distance b/w two cities, O(1) 
def distance(nodei, nodej):
	return sqrt((cities[nodej][0] - cities[nodei][0])**2 + (cities[nodej][1] - cities[nodei][1])**2)

#init: solution for testTsp.txt ~= 84.3460, Time ~= 30.7361
#solution for tsp.py ~= 26442.7303, Time ~= 45338.6414 s ~= 12.595 h (not sure)
if __name__ == '__main__':
	draft, cities = open('tsp.txt').read().splitlines(), {}
	for line, i in zip(draft[1:], range(1, int(draft[0]) + 1)):
		cities[i] = list(map(float, line.split()))

	startTime = process_time()
	print(tsp(cities))
	print(process_time() - startTime)
