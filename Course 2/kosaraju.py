'''kosaraju.py: Graph Theory'''

'''Slick algorithm for finding all SCCs in a given directed graph in a fast O(m + n) run time;
since it's based on dfs'''

'''https://www.ics.uci.edu/~pattis/ICS-33/lectures/complexitypython.txt'''

#main func for kosaraju algorithm; managing first and second passes of graph
def kosaraju(graph):
	#because leader is reassigned
	global leader

	if firstpass:
		for node in range(1, 10 + 1):
			if not explored[-1 * node]:
				dfs(graph, node)
	else:
		#iterating nodes from their largest finish time to smallest
		for node in reversed(finishTimes):
			if not explored[-1 * node]:
				leader = node
				dfs(graph, node)

#modified dfs func, managing both first and second pass book-keeping
def dfs(graph, start):
	explored[-1 * start] = True

	#creating sccs of graph in second pass
	if not firstpass:
		if leader not in sccs:
			sccs[leader] = [start]
		else:
			sccs[leader].append(start)

	#if there's an scc with only one node, it's basically a sink node in graph or graph_rev
	if start in graph:
		for v in graph[start]:
			if not explored[-1 * v]:
				dfs(graph, v)

	if firstpass:
		#magic ordering for second pass of kosaraju!
		finishTimes.append(start)

#init
if __name__ == '__main__':
	graph, draft = {}, open('directedGraph (scc, 10).txt').read().splitlines()

	for line in draft:
		edge = list(map(int, line.split()))
		if edge[0] not in graph:
			graph[edge[0]] = [edge[1]]
		else:
			graph[edge[0]].append(edge[1])

	graph_rev = {}
	for node in graph:
	    for edge in graph[node]:
	        if edge not in graph_rev:
	            graph_rev[edge] = []
	        graph_rev[edge].append(node)

	explored, finishTimes, firstpass = [False] * 10, [], True
	leader, sccs = None, {}

	kosaraju(graph_rev)
	firstpass, explored = not firstpass, [False] * 10
	kosaraju(graph)

	print(sccs)
