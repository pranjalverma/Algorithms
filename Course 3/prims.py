'''prims.py: Graph Theory/Greedy Algorithm'''

'''@author: Pranjal Verma'''

'''In the naïve implementaion, similar to the naïve version of dijkstra, when X (explored) has
at least n/2 vertices in it (event), we're already looking at O(n) vertices and all their edges,
because the graph is at least weakly connected and we're only looking at crossing edges 
in this slightly better implementation, instead of even more naïvely iter-ing over all edges 
to first find crossing edges. So total run-time is dominated by O(n^2) after this event, and 
this bound can be tightned by O(nm)!'''

'''You can select blocks of code to put inside a type of bracketing and then bracket this block'''

from math import inf
from heapq import heappush, heappop, heapify, _siftdown, _siftup
from time import time
from collections import defaultdict

def prims(graph):
	start = list(graph)[0]
	explored, treeCosts = set([start]), []

	unexplored = []
	for v in graph[start]:
		heappush(unexplored, [v[1], v[0]])

	while explored != set(graph):
		winner = heappop(unexplored)

		explored |= set([winner[1]])
		treeCosts.append(winner[0])

		for v in unexplored:
			if v[1] == winner[1]:
				v[0] = inf
				#heapdelete(unexplored, unexplored.index(v))
		heapify(unexplored)

		for v in graph[winner[1]]:
			if v[0] not in explored:
				heappush(unexplored, [v[1], v[0]])

	return sum(treeCosts)

def heapdelete(heap, i): #verify with "heapq"
	heap[i][0], parent = -inf, (i - 1) // 2
	while i != 0 and heap[parent][0] >= heap[i][0]:
		heap[parent], heap[i] = heap[i], heap[parent]
		i = parent
		parent = (i - 1) // 2

	heappop(heap)

#naïve prim's, brute-forcing over all crossing edges; O(nm), explaination above!
def badPrims(graph):
	explored, treeCosts = set([list(graph)[0]]), []

	#until all vertices are covered; property of any spanning tree
	while explored != set(graph):
		bestCost, winner = inf, None

		for u in explored:
			for v in graph[u]:
				if v[0] not in explored:
					#remembering cheapest edge
					if v[1] < bestCost:
						bestCost = v[1]
						winner = [u]
						winner.extend(v)

		explored |= set([winner[1]])
		treeCosts.append(winner[2])

	#returning sum of all costs of edges we chose for MST!
	return sum(treeCosts)

#init
if __name__ == '__main__':
	draft, graph = open('undirectedGraph (weighted, 500).txt').read().splitlines(), defaultdict(list)

	for line in draft[1:]:
		edge = list(map(int, line.split()))
		graph[edge[0]].append(edge[1:])
		graph[edge[1]].append([edge[0], edge[2]])

	startTime = time()
	print('Bad prims: ' + str(badPrims(graph)) + ', ' + 'Time: ' + str(time() - startTime))

	startTime = time()
	print('Good prims: ' + str(prims(graph)) + ', ' + 'Time: ' + str(time() - startTime))

