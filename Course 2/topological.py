'''topological.py: Graph Theory'''

'''OMFG please fucking remember CMD + [ or CMD + ] to indent entire blocks of code'''

'''Linear time: O(m + n)'''

'''calling dfs on all unexplored nodes, dfs finding everything findable from "node"; basically
managing all sccs in graph'''
def sort(graph):
	for node in range(1, 5 + 1):
		if not explored[-1 * node]:
			dfs(graph, node)

#dfs for traversal
def dfs(graph, start):
	explored[-1 * start] = True

	'''get() returns None as default value if key isn't in graph; bool(None) is False; thus
	handling keyError that's seen in case of directed graphs'''
	if graph.get(start):
		for v in graph.get(start):
			if not explored[-1 * v]:
				dfs(graph, v)

	#adding sinks of graph at each recursive stack depth, thus creating a topological ordering
	order.append(start)

#init
if __name__ == '__main__':
	graph, draft = {}, open('directedGraph (acyclic, 5).txt').read().splitlines()

	for line in draft:
		edge = list(map(int, line.split()))
		if edge[0] not in graph:
			graph[edge[0]] = [edge[1]]
		else:
			graph[edge[0]].append(edge[1])

	explored, order = [False] * 5, []
	sort(graph)
	print(order)