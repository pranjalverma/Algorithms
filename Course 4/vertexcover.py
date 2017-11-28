'''vertexcover.py: NP-Complete'''

'''@author: Pranjal Verma'''

'''
	Trees:
	http://www.geeksforgeeks.org/vertex-cover-problem-set-2-dynamic-programming-solution-tree/

	.txt files for trees will contain edges from root to leaves, thus root is always processed
	first, acc. to the link above^
'''

'''
	Running time, O(m*2^size):
	Exponential time; every recursive call occurs for a size that is 1 less than that of it's
	parent call. Thus, acc. to the recursion tree there'll be O(2^size) num of recursive calls
	before reaching any base-case and the height of this binary recursion tree will be 'size';
	binary tree because there are two recursive calls! There's O(m) work for every recursive
	call, thus total running time becomes O(m*2^size).

	This algorithm is polynomial time as long as size = O(log(n)), so that time = O(m*n). If
	the vertex cover of a graph has size more than this, this algorithm becomes infeasible.

	Also, much better than the naïve brute-force time of O(n^size), which comes from taking
	combinations of 'size' from n aka n-choose-size. This is basically trying all possibilities!
'''

'''
	Difference b/w empty vertex cover and raising exceptiong:
	An empty vertex cover can occur in case of a graph with no edges, where no vertices are
	required to cover all edges, because there are none!

	But, failing to find a valid vertex cover for the edges and thus raising an exception means
	the there's no set of vertices, including the empty set, than can cover all edges of the 
	graph.
'''

#sub-optimal O(m*2^size) algorithm for the Vertex Cover Problem
#works only when size is small
#can be made optimal using memoisation
def findCover(graph, size):

	#BASE CASES:

	#graph with no edges; return cover of size 0
	if not graph:
		return set(['empty'])

	#graph with only 1 edge
	if len(graph) == 1:
		return set(list(graph)[0][0])

	#graph with 2 edges and size limit of vertex cover = 1 (or 0)
	if size < 2 or len(graph) < 3:

		#list of nodes acc to edges in graph
		nodeList = []
		for edge in graph:
			nodeList.extend(edge)

		#getting the 'mode' of nodeList; i.e most occuring vertex
		candidate = max(set(nodeList), key=nodeList.count)

		#if occurrence of 'mode' = num of edges in graph
		#i.e if 'mode' occurs in all edges of graph
		#include 'mode' in vertex cover
		if nodeList.count(candidate) == len(graph):
			return set([candidate])

		#else no cover exists!
		else:
			raise Exception('No such Vertex Cover found!')

	#MAIN RECURSION:

	#choosing 0th edge incase given graph is a tree; explaination above^
	#following two recursive calls then represent cases where root is either included
	#or excluded!
	u, v = list(graph)[0]

	#recursive call on graph without u; including u if a subCover exists for this graph
	subCover = findCover({edge for edge in graph if u not in edge}, size - 1)
	if subCover:
		return (subCover - {'empty'}) | set([u])

	#recursive call on graph without v; including v if a subCover exists for this graph
	subCover = findCover({edge for edge in graph if v not in edge}, size - 1)
	if subCover:
		return (subCover - {'empty'}) | set([v])

#init
if __name__ == '__main__':
	draft, graph = open('undirectedGraph (8, vertex weighted).txt').read().splitlines(), set()

	numNodes = draft[0].split()[0]
	for line in draft[1:]:
		graph |= set([tuple(map(int, line.split()))])

	print('Minimum weight Vertex Cover for given graph: ' + str(findCover(graph, 7)))
