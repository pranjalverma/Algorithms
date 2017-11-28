'''dijkstra.py: Graph Theory/Greedy Algorithm'''

'''@author: Pranjal Verma'''

'''The the naïve implementation of Dijkstra, the run time is Θ(nm) because the outer loop runs 
(n - 1) times until all vertices are sucked up in X, the group of vertices which have already
been handled, and in each iteration we look at all m edges to see if they cross the frontier
and if yes, we compute their dijkstra score, which in turn takes O(1).

Even IF we optimise it by looking at edges of ONLY vertices currently in X at each outer loop
iteration, the runtime would still be far from O(mlogn) because from and beyond the point where
X has at least n/2 vertices, the num of edges brute-forced is already O(m) and not O(1), untike
for when X has less than n/2 vertices, because at this point we're already looking at edges of
O(n) vertices!'''

from math import inf
from heapq import heappush, heappop
from time import time

'''badass, slick implementation of dijkstra, running time a much better O(mlogn);
actually O((m + n)logn) for m + n heap operations, but since there's a path from start to all 
other vertices, it's at least a weakly connected graph, thus m will dominate over n, making 
O(m + n) = O(m)'''
def dijkstra(graph, start):
	explored, distances = [start], {}
	distances[start] = 0

	#heap for crossing edges, each heap operation taking O(logn) time
	unexplored = []
	for w in graph[start]:
		heappush(unexplored, (distances[start] + w[1], w[0]))

	while set(explored) != set(graph):
		#(n - 1) operations in overall algo
		winner = heappop(unexplored)

		explored.append(winner[1])
		distances[winner[1]] = winner[0]

		for v in graph[winner[1]]:
			if v[0] not in explored:
				'''m operations in overall algo, since once edge is added to X, it's never 
				seen again!'''
				heappush(unexplored, (winner[0] + v[1], v[0]))

	return distances[7] #2599

#naïve implementation of dijkstra, running in O(nm), explaination above!
def badDijkstra(graph, start):
	explored, distances = [start], {}
	distances[start] = 0

	#until all shortest paths are computed
	while set(explored) != set(graph):
		greedyScore, winner = inf, None

		for v in explored:
			for w in graph[v]:
				if w[0] not in explored:
					#remembering best greedy score and it's edge
					if distances[v] + w[1] < greedyScore:
						greedyScore = distances[v] + w[1]
						winner = w[0]

		explored.append(winner)
		distances[winner] = greedyScore

	return distances[7] #2599

#init
if __name__ == '__main__':
	graph, draft = {}, open('undirectedGraph (weighted, 200).txt').read().splitlines()

	for line in draft:
		adjList = line.split('\t', maxsplit=1)
		vals = adjList[1].split('\t')
		vals.pop()
		graph[int(adjList[0])] = [list(map(int, nodeLenPair.split(','))) for nodeLenPair in vals]

	startTime = time()
	print(dijkstra(graph, 1))
	print(time() - startTime)

	startTime = time()
	print(badDijkstra(graph, 1))
	print(time() - startTime)
