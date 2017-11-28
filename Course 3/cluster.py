'''cluster.py: Graph Theory/Greedy Algorithm/Data Structure'''

'''@author: Pranjal Verma'''

'''discovered using 'int' as: int('num as string', base of input); int('111', 2) = 7'''

from collections import defaultdict, OrderedDict
from operator import itemgetter
from time import time

#union find data structure optimised for max-spacing k-clustering using single link clustering
#lazy union-find using union by ranks
class UnionFind():

	#ranks and parents for each obj
	#augmented to keep track of current num of clusters
	def __init__(self):
		self.parents = defaultdict(int)
		self.ranks = defaultdict(int)
		self.clusterCount = 0

	#insert new obj in it's own cluster
	def insert(self, node):
		if node not in self.parents:
			self.parents[node] = node
			self.ranks[node] = 0
			self.clusterCount += 1

	#find root of nodes of given edge, wrapper for '_findRoot()'
	def find(self, edge):
		return self._findRoot(edge[0]), self._findRoot(edge[1])

	#helper func for 'find()'
	def _findRoot(self, node):
		ptr = ptr1 = node
		while self.parents[ptr] != ptr:
			ptr = self.parents[ptr]

		return ptr

	#for merging two clusters, using ranks of root nodes 
	def union(self, parent1, parent2):
		newRoot = None

		#ranks only change when two clusters with root nodes 
		#having equal ranks are merged!
		if self.ranks[parent1] == self.ranks[parent2]:
			self.parents[parent2] = parent1
			self.ranks[parent1] += 1
			newRoot = parent1

		elif self.ranks[parent1] > self.ranks[parent2]:
			self.parents[parent2] = parent1
			newRoot = parent1

		else:
			self.parents[parent1] = parent2
			newRoot = parent2

		self.clusterCount -= 1
		return newRoot

#cluster func; O(mlogn)
#m = num of union+find operations, or num of dist func values encountered, or num of edges
#n = num of nodes in graph
def cluster(graph):
	#sorting to always encounter current spacing among clusters
	clusters, sortedGraph = UnionFind(), OrderedDict(sorted(graph.items(), key=itemgetter(0)))

	#creating initial, lonely clusters
	for cost in sortedGraph:
		for edge in sortedGraph[cost]:
			clusters.insert(edge[0])
			clusters.insert(edge[1])

	#iterating over current spacings
	for cost in sortedGraph:

		#accounting that some spacings can be associated with multiple pairs of nodes
		for edge in sortedGraph[cost]:

			#finding roots of given spacing nodes
			#pair considered only if they're in different clusters!
			u, v = clusters.find(edge)
			if u != v:

				#if required clusters-count is reached, return current spacing
				#this is the max-spacing needed for 4-clustering
				if clusters.clusterCount == 4:
					return cost

				#if required cluster-count is yet to be attained:
				#take union of clusters connected by given edge
				clusters.union(u, v)

def bigCluster(graph):
	clusters = UnionFind()

	for node in graph:
		clusters.insert(node)

	tracker = list(graph)
	for nodei in graph:
		if nodei in tracker:
			peers = generateFromData(int(graph[nodei], 2), graph, 24)
			for nodej in peers:
				if nodej in tracker:
					clusters.union(nodei, nodej)
					tracker.remove(nodej)

			while peers:
				for nodex in peers:
					peers.remove(nodex)
					peersDeep = generateFromData(int(graph[nodei], 2), graph, 24)
					for nodey in peersDeep:
						if nodey in tracker and nodey != nodei:
							clusters.union(nodex, nodey)
							tracker.remove(nodey)
							peers.append(nodey)

	return str(str(clusters.clusterCount) + ', ' + str(len(tracker)))

'''def findPeers(binary, spacing, graph):
	peers = []

	if spacing == 1:
		for i in range(24):
			peer = list(binary)
			peer[i] = str(int(not int(peer[i])))
			peer = int(''.join(peer), 2)
			if peer in graph and peer != int(binary, 2):
				peers.append(peer)
	else:
		for j in range(1, 24):
			for i in range(0, 24, j):
				peer = list(binary)
				peer[j] = str(int(not int(peer[j])))
				peer[i] = str(int(not int(peer[i])))
				peer = int(''.join(peer), 2)
				if peer in graph and peer != int(binary, 2):
					peers.append(peer)

	return peers'''

def generateNumsWith12Diff(num, n_bits):
	""" generates list containing numbers differing from num with 1 or 2 bits (where n_bits is number of bits representing num) """
	resultList = []
	for i in range(n_bits):
		resultList.append(num ^ 2**i)
	for i in range(n_bits - 1):
		for j in range(i + 1, n_bits):
			resultList.append(num ^ (2 ** i + 2 ** j))
	return resultList

def generateFromData(num, graph, n_bits):
	""" generates list containing numbers differing from num with 1 or 2 bits (where n_bits is number of bits representing num) 
	
	but only if they are in data"""
	resultList = []
	differing = generateNumsWith12Diff(num, n_bits)
	for i in differing:
		if i in graph:
			resultList.append(i)
	return resultList

#init
if __name__ == '__main__':
	draft, graph = open('cluster.txt').read().splitlines(), defaultdict(list)

	for line in draft[1:]:
		edge = list(map(int, line.split()))
		graph[edge[2]].append(tuple(edge[:2]))

	startTime = time()
	print('Max spacing for 4-clustering: ' + str(cluster(graph)) + ', Time: ' + str(time() - startTime))

	draft, graph = open('bigCluster.txt').read().splitlines(), defaultdict(str)

	i = 0
	for line in draft[1:]:
		binary = ''.join(line.split())
		if binary not in graph.values():
			graph[i] = binary
			i += 1

	startTime = time()
	print('k-clustering for max-space of 3 is: k = ' + str(bigCluster(graph)) + ', Time: ' + str(time() - startTime))
