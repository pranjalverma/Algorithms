'''bellmanford.py: Dynamic Programming/Graph Theory'''

'''@author: Pranjal Verma'''

'''seems like a O(n^3) algo but m = O(n^2) in dense connected graphs so a tighter bound of
O(mn) can be established'''

'''
	Extra +1 in for-loop:
	is for taking pathLen to 'n' in the last step, to check for -ve cycles if any value for
	pathLen = n-1 is different from that of pathLen = n, there's a -ve cycle because then in
	this last step we could travel on this -ve cycle, revisiting some node and reduce the 
	value, and thus changing the path that was logged for pathLen = n-1
	Changing of entire path b/w these two steps is crucial but subtle, and it may happens every
	time pathLen changes, not just for n-1 and n. Going from n-1 to n gives only one extra edge
	that can be added to out path, but a cycle must have more than 2 edge, so entire path is
	altered to accomodate a cycel where nodes can be revisited. If this cycle happens to be -ve
	value will change and this cycle will be detected! 
'''

'''TODO: check -ve cycles extention, once graph for it is obtained'''

from math import inf
from time import time

#naïve O(mn) Bellman and Ford's single-source shortest path algorithm!
#can be improved with 'stopping early' and O(n)-array cache optimisations
#this space optimisations will not help reconstruct actual paths tho
def bellmanford(graph, source):

	#init
	cache, n = {}, len(graph)
	cache[0, source] = 0
	for node in graph:
		if node != source:
			cache[0, node] = inf

	#for all possible shortest-path lengths; can't be  more than (n - 1)
	#otherwise we're revisiting a node
	#extra +1 in for-loop explained above
	for pathLen in range(1, (n - 1 + 1) + 1):

		#for all nodes of graph in this path length range
		for node in graph:

			#O(n) recurrence because of the second min() condition
			cache[pathLen, node] = min(cache[pathLen - 1, node],
										min([cache[pathLen - 1, w] + v[1] 
											for w in graph
											for v in graph[w]
											if v[0] == node]))
	
	#detecting negative cycles in graph
	if cache[n - 1, 7] == cache[n, 7]:
		return reconstruct(cache, graph, source, 7), cache[len(graph) - 1, 7] #2599
	else:
		return 'Negative Cycle Detected'

#optimised Bellman-Ford Algorithm, O(mn) (with huge constant-factor savings for dense graphs!)
#time-optimised by 'stopping early' once shortest path values get repeated for next 'pathLen'
#space-optimised by using only O(n)-array cache instead of O(n^2) table as in above algo 
def optimisedBellmanford(graph, source):

	#init; 'explored' keeps track of nodes for which shortest paths have already been 
	#computed in previous limits for pathLen, in the outer for-loop
	cache, explored = [0] * len(graph), set([source])
	for node in graph:
		if node != source:
			cache[-1 * node] = inf
		else:
			cache[-1 * node] = 0

	#pathLen limits as above algo
	for pathLen in range(1, (len(graph) - 1) + 1):

		#testing all nodes of graph for each pathLen limit as above algo
		for node in graph:

			#stopping early: applying recurrence to node only if it's shortest path
			#has NOT already been computed!
			if node in explored:
				continue

			#if not in explored, tracking it's current value and applying O(n) recurrence on node!
			previous = cache[-1 * node]
			cache[-1 * node] = min(cache[-1 * node],
									min(cache[-1 * w] + v[1] for w in graph
										for v in graph[w]
										if v[0] == node))

			#if previous value same is current value, marking node as explored
			#so as to avoid it in all further iterations of pathLen
			if previous == cache[-1 * node] and previous != inf:
				explored |= set([node])

	return cache[-1 * 7] #2599

#O(n) reconstruction algorithm for constructing path from source to sink from given cache
#cache needs to be complete for all previous pathLen limits
def reconstruct(cache, graph, source, sink):

	#array to store path from source to sink
	path, n = [str(sink)], len(graph)

	#if no path
	if cache[n - 1, sink] == inf:
		return 'No path exists from ' + str(source) + ' to ' + str(sink) + '!'

	#if finite path exists
	else:
		#init: nodej is sink and nodei is gonna be the node just before nodej in
		#source -> sink shortest path
		pathLen, nodej, nodei = n - 1, sink, None

		#continue preceding in cache table from sink until source is encountered 
		while nodei != source:

			#init: currCost helps decide which minimum was used in recurrence
			nodei, currCost = None, inf

			#if previous value is different than current:
			if cache[pathLen, nodej] != cache[pathLen - 1, nodej]:
				for w in graph:
					for v in graph[w]:
						if v[0] == nodej and cache[pathLen - 1, w] + v[1] < currCost:
							currCost = cache[pathLen - 1, w] + v[1]
							nodei = w

				#update path and nodej
				path.append(str(nodei))
				nodej = nodei

			#moving backwards in cache from pathLen = n-1 to pathlen = 0!
			pathLen -= 1

	#return pretty-printed path
	return ' -> '.join(reversed(path))

#init
if __name__ == '__main__':

	#using same graph as in dijkstra.py
	draft, graph = open('undirectedGraph (weighted, 200).txt').read().splitlines(), {}
	for line in draft:
		adjList = line.split('\t')
		adjList.pop()
		graph[int(adjList[0])] = [list(map(int, edge.split(','))) for edge in adjList[1:]]

	startTime = time()
	print('Optimised Bellman-Ford: ' + str(optimisedBellmanford(graph, 1)))
	print('Time: ' + str(time() - startTime))

	startTime = time()
	result = bellmanford(graph, 1)
	endTime = time()
	print('Bellman-Ford: ' + str(result[1]))
	print('Time: ' + str(endTime - startTime))

	print('Path from 1 to 7: ' + str(result[0]))
