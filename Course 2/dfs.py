'''dfs.py: Graph Theory'''

'''Runs in time O(m + n)'''

#dfs for graph traversal
def dfs(graph, start):
	explored[-1 * start] = True
	for v in graph[start]:
		if not explored[-1 * v]:
			
			#recursive nature of DFS creates an implicit stack, unlike the explicit queue of BFS
			dfs(graph, v)

	#returns True if all nodes are explored
	return not False in explored

#init
if __name__ == '__main__':
	graph, draft = {}, open('undirectedGraph (200).txt').read().splitlines()
	
	for line in draft:
		adList = line.split('\t', maxsplit=1)
		vals = adList[1].split('\t')
		vals.pop()
		graph[int(adList[0])] = list(map(int, vals))

	#global variable for tracking visited nodes
	explored = [False] * 200
	print(dfs(graph, 1))
