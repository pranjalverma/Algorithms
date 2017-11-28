'''kargermincut.py: Randomisation'''

'''Counts no. of crossing edges in the min cut of given undirected graph by contracting 
randomly chosen edges with a success probability of i/n^2 which can be boosted to a better 
1/n by repeated trails ((n^2)logn trails approx.)'''

'''Runs in time Ω((n^2)mlogn), considering the trails and that it will at least look at Ω(m)
edges in it's execution, again considering parallel edges, it can be more'''

from random import choice

#main func for karger's algo; still better than brute force which is O(2^n)
def kargermincut(graph):
	results = []
	while len(graph) > 2:
		#choosing random edge
		vertex = choice(list(graph.keys()))
		edge = (vertex, choice(graph[vertex]))

		#edge contraction with house-keeping
		graph[edge[0]].extend(graph[edge[1]])
		for vertex in graph[edge[1]]:
			graph[vertex].remove(edge[1])
			graph[vertex].append(edge[0])

		#deleting self-loops
		while edge[0] in graph[edge[0]]:
			graph[edge[0]].remove(edge[0])

		#deleting vertex that was merged into supernode 
		del graph[edge[1]]

	#finding no. of crossing edges
	for vertex in graph.keys():
		results.append(len(graph[vertex]))

	return results

#init
if __name__ == '__main__':
	draft, graph = open('kargerMinCut (200).txt').read().splitlines(), {}
	
	for line in draft:
		adList = line.split('\t', maxsplit=1)
		vals = adList[1].split('\t')
		vals.pop()
		graph[int(adList[0])] = list(map(int, vals))

	print(kargermincut(graph), graph)
