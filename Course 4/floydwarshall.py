'''floydwarshall.py: Dynamic Programming/Graph Theory'''

'''@author: Pranjal Verma'''

'''
	-ve cycles:
	For any i-j shortest path where i = j, the value has to be 0 (taking the empty path from
	i to itself). If you start from i and go towards any other node != i (where i=j), in order
	to come back to i you HAVE to traverse a cycle. If this cycle is NOT a -ve cycle, the cost
	of this cycle-path will be greater than 0, thus rendering the shortest i-i path to still be
	the empty path with cost 0.

	BUT if this cycle was a -ve cycle from i to itself, the new cost will be less than the cost
	of the empty path (i.e less than 0). 

	Thus, if any value on the diagonal of our 3D cache is -ve, the path with this -ve cost MUST
	include a -ve cycle. Thus by checking these diagonal i-i values, we can detect whether our
	graph has -ve cycles or not!
'''

from math import inf
from time import time

#naïve O(n^3) Floyd-Warshall Algorithm for All-Pair Shortest Path problem!
def floydwarshall(graph):

	#init
	cache, n = {}, len(graph)

	#BASE CASES:

	#for all i, j pair of nodes in graph, and for maxLabel = 0
	#i.e no internal nodes in i-j path
	#internal nodes exclude i and j
	for nodei in graph:
		for nodej in graph:

			#if i == j, shortest path value is 0 cuz i/j can reach itself via the empty path
			if nodei == nodej:
				cache[nodei, nodej, 0] = 0

			#else, either there's a direct i-j edge or there isn't
			else:

				#finding that direct edge, if it exists
				costij = [nodeCostPair[1] for nodeCostPair in graph[nodei]
											if nodeCostPair[0] == nodej]

				#if single-valued list 'costij' is not empty then
				#i-j path with no internal nodes has cost = cost of that direct i-j edge
				if costij:
					cache[nodei, nodej, 0] = costij[0]

				#there's no i-j path with 0 internal nodes, thus current value is inf
				else:
					cache[nodei, nodej, 0] = inf

	#MAIN TRIPLE-LOOP:

	#maxLabel loop HAS to be first because that's what maintains the ordering of
	#subproblems, i.e ensures that smaller subproblems are solved before larger ones!
	for maxLabel in graph:

		#for every i, j pair of nodes in graph; ordering of these two loops doesn't matter
		for nodei in graph:
			for nodej in graph:

				#O(1) time recurrence to fill in 3D table
				cache[nodei, nodej, maxLabel] = min(cache[nodei, nodej, maxLabel - 1],
													cache[nodei, maxLabel, maxLabel - 1]
													+ cache[maxLabel, nodej, maxLabel - 1])

	#detecting negative cycles as explained above
	if min([cache[i, i, n] for i in graph]) > -1:
		return cache[1, 7, n] #2599
	else:
		return 'Negative Cycle Detected!'

#init
if __name__ == '__main__':
	draft, graph = open('undirectedGraph (weighted, 200).txt').read().splitlines(), {}
	for line in draft:
		adjList = line.split('\t')
		adjList.pop()
		graph[int(adjList[0])] = [list(map(int, edge.split(','))) for edge in adjList[1:]]

	startTime = time()
	print('Floyd-Warshall: ' + str(floydwarshall(graph)))
	print('Time: ' + str(time() - startTime))
