'''bfs.py: Graph Theory'''

'''Both algorithms here are variations of standard BFS with differentiating constant factors so
they both run in time linear in m & n, i. e, O(m + n)'''

from math import inf

#bfs for graph traversal
def bfs(graph, start):
	queue, explored[-1 * start] = [start], True

	'''most pythonic way of checking if a sequence is empty or not; empty sequences 
	are implicitly false: https://stackoverflow.com/questions/53513/best-way-to-check-if-a-list-tuple-or-dict-is-empty'''
	while queue:
		v = queue.pop(0) #popping like a queue!
		for w in graph[v]:
			if not explored[-1 * w]:
				explored[-1 * w] = True
				queue.append(w)

	#checking if all nodes have been explored or nah; returns True if yes
	return not False in explored

#bfs for computing shortest paths from given source; only good if each edge has length 1
def shortestPath(graph, start, end):
	distances = [inf] * 200
	queue, distances[-1 * start], explored[-1 * start] = [start], 0, True

	while queue:
		v = queue.pop(0)
		for w in graph[v]:
			if not explored[-1 * w]:
				#updating dist(w) in terms of dist(v) as bfs works in layers
				distances[-1 * w], explored[-1 * w] = distances[-1 * v] + 1, True
				queue.append(w)

	#return required distance
	return distances[-1 * end]

#init
if __name__ == '__main__':
	graph, draft = {}, open('undirectedGraph (200).txt').read().splitlines()

	for line in draft:
		adList = line.split('\t', maxsplit=1)
		vals = adList[1].split('\t')
		vals.pop()
		graph[int(adList[0])] = list(map(int, vals))

	explored = [False] * 200
	print('Graph traversed? ' + str(bfs(graph, 1)))
	explored = [False] * 200
	print('Shortest Path from 1 -> 200: ' + str(shortestPath(graph, int(input('Start node: ')), 
		int(input('End node: ')))))


