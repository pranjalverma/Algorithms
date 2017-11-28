'''johnson.py: Dynamic Programming/Graph Theory/Greedy Algorithm'''

'''@author: Pranjal Verma'''

'''
	Working:
	Works in (n + 1) passes, one to bellmanford and n to dijkstra:

	FIRST there's a call to bellmanford(), using a dummy nodes as the source vertex. (O(mn))
	This dummy node is made to have out-going arcs to every other node in the graph but have
	no incoming arcs, thus making it invisible from the graph's point of view! bellmanford()
	is then run to find the shortest paths to all the nodes of this graph. If the graph has
	a negative cycle, it's detected in this pass and the program halts with an exception!
	Otherwise all the shortest paths from this dummy node to all other nodes are computed
	and these shortest paths form the weights for every corresponding node in the graph,
	which are crucial for Johnson's Algorithm, i.e the shortest path from dummy node to say
	a node X is now the weight of this node X. If L is a path length for nodes s and t, then
	under this weighting, the new path length is:

							L' = L + weight_s - weight_t

	Thus, all s-t paths are shifted by a constant factor and shortest paths are preserved but
	all edges are now make +ve! So now we can run dijkstra on this graph!

											****

	NEXT there are n calls to dijkstra(), where every node is considered a source and it's
	shortest paths to every other node are computed in O(mlogn) time, which is the best! Also,
	in a final step all dijkstra-computed paths are shifted back by a factor of:

							|Shift| = weight_s - weight_t

	To get all-pair shortest paths wrt the original given graph.

											****

	This particular implementation of Johnson's Algorithm computes not only all-pair shortest
	paths but also the 'Shortest Shortest Path', which as the name suggests, is the smallest
	shortest path out of all computed shortest paths, for the given graph!
'''

from math import inf
from time import time
from collections import defaultdict
from heapq import heappop, heappush

#Efficient O(nmlogn) Johnson's Algorithm for the All-Pair Shortest Paths problem!
#Working explained above^
def johnson(graph):

	#O(n) step for adding the dummy node to be used as source in bellmanford()
	graph[0].extend([[i, 0] for i in graph if i != 0])
	graph[0].append([0, 0]) #to avoid empty seq for min()

	#O(mn) call to bellmanford() as explained above^ under 'Working'
	nodeWeights = bellmanford(graph, 0)
	del graph[0]

	#init
	newGraph, shortestPaths = defaultdict(list), {}
	n = len(graph)

	#nodeWeights is a *non-empty* list if there's no negative cycle in graph, 
	#therefore, bool(nodeWeights) == True
	#O(n^2) + O(nmlogn) + O(n^2) = O(nmlogn) time overall!
	if nodeWeights:

		#O(n^2); constructing new graph with all +ve edges, using accuired node weights
		#can run dijkstra on this graph now
		for i in graph:
			for j in graph[i]:
				newGraph[i].append([j[0], j[1] + nodeWeights[-1 * i] - nodeWeights[-1 * j[0]]])

		#O(nmlogn) + O(n^2) = O(nmlogn) step
		#dijkstra is run n times, considering each node as source once
		for source in newGraph:

			#O(mlogn)
			shortestPaths[source] = dijkstra(newGraph, source)

			#O(n)
			for sink in newGraph:
				shortestPaths[source][sink] -= nodeWeights[-1 * source] - nodeWeights[-1 * sink] 

		#container for shortest shortest paths considering every node as a source
		#O(n^2)
		minPaths = []
		for dists in shortestPaths.values():
			minPaths.append(min(list(dists.values())))

		#returning the shortest shortest path overall! O(n)
		return min(minPaths)

	#otherwise nodeWeights is 'False', in which case it raises exception and halts program!
	else:
		raise Exception('Negative Cycle Detected!')

#optimised Bellman-Ford Algorithm, O(mn) (with huge constant-factor savings for dense graphs!)
#time-optimised by 'stopping early' once shortest path values get repeated for next 'pathLen'
#space-optimised by using only O(n)-array cache instead of O(n^2) table as in above algo 
def bellmanford(graph, source):

	#init; 'explored' keeps track of nodes for which shortest paths have already been 
	#computed in previous limits for pathLen, in the outer for-loop
	cache, explored, n, pastCache = [0] * len(graph), set([source]), len(graph), []
	for node in graph:
		if node != source:
			cache[-1 * node] = inf
		else:
			cache[-1 * node] = 0

	#pathLen limits as above algo
	for pathLen in range(1, n + 1):

		#testing all nodes of graph for each pathLen limit as above algo
		for node in graph:

			#stopping early: applying recurrence to node only if it's shortest path
			#has NOT already been computed!
			if node in explored:
				continue

			#tracking previous values of shortest paths to help detect -ve cycles
			pastCache = list(cache)

			#if not in explored, tracking it's current value and applying O(n) recurrence on node!
			previous = cache[-1 * node]
			cache[-1 * node] = min(cache[-1 * node],
									min([cache[-1 * w] + v[1]
										for w in graph
										for v in graph[w]
										if v[0] == node]))

			#if previous value same is current value, marking node as explored
			#so as to avoid it in all further iterations of pathLen
			if previous == cache[-1 * node] and previous != inf:
				explored |= set([node])

	#return shortest paths if values of (n-1)th iter = values of extra nth iter
	#see bellmanford.py or online for explaination on detecting -ve cycles in bellmanford
	if pastCache == cache:
		print('Sent Cache, large')
		return cache

	#else if !=, there are some negative cycles that were traversed that resulted in 
	#these changes; return False
	else:
		print('Sent False, large')
		return False

#optimised implementation of dijkstra, O(mlogn)
def dijkstra(graph, start):

	#init
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

	return distances

#init
if __name__ == '__main__':
	draft, graph = open('large.txt').read().splitlines(), defaultdict(list)
	for line in draft[1:]:
		edge = list(map(int, line.split()))
		graph[edge[0]].append(edge[1:])

	startTime = time()
	print('Shortest Shortest Path for large.txt: ' + str(johnson(graph)))
	print('Time: ' + str(time() - startTime))
