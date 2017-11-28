'''mwis.py: Dynamic Programming'''

'''@author: Pranjal Verma'''

'''DP algorithm for finding max-weight independent set (MWIS) in a given path graph'''

'''
	Python For-Loops:
	The for statement in Python differs a bit from what you may be used to in C or Pascal. 
	Rather than always iterating over an arithmetic progression of numbers (like in Pascal), 
	or giving the user the ability to define both the iteration step and halting condition 
	(as C), Python's for statement iterates over the items of any sequence (a list or a string), 
	in the order that they appear in the sequence!
'''

from time import time

#O(n) func to find MWIS (max-weight set of nodes of graph with no adjacent nodes!)
#only find the max-weight of this set
def find(graph):
	#solution table and init
	subsolutions = {}
	subsolutions[0], subsolutions[1] = 0, graph[1]

	#filling table iteratively, reducing redundancy of brute-force solution!
	for i in range(2, numNodes + 1):
		subsolutions[i] = max(subsolutions[i - 1], subsolutions[i - 2] + graph[i])

	#reconstructing mwis and returning
	return reconstruct(subsolutions), subsolutions[numNodes]

#reconstructs the actual MWIS from the sub-soluton table generated in find(), in O(n)
#re-reading the table like this is faster than the augmentation solution!
def reconstruct(subsolutions):
	mwis, i = set(), 1000
	while i >= 2:
		if subsolutions[i - 1] >= subsolutions[i - 2] + graph[i]:
			i -= 1
		else:
			mwis |= set([i])
			i -= 2

	#if node 2 not in mwis, then node 1 should be!
	if i not in mwis:
		mwis |= set([1])
		
	return mwis

#init
if __name__ == '__main__':
	draft, graph, check = open('mwis.txt').read().splitlines(), {}, [1, 2, 3, 4, 17, 117, 517, 997]

	numNodes = int(draft[0])
	for line, i in zip(draft[1:], range(1, numNodes + 1)):
		graph[i] = int(line)

	startTime = time()
	mwis = find(graph)
	endTime = time()

	print('Answer: ' + ''.join([str(int(i in mwis[0])) for i in check])
	 + ', ' + 'MW: ' + str(mwis[1]))
	print('Time: ' + str(endTime - startTime))
