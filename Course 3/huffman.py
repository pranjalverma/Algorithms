'''huffman.py: Greedy Algorithm'''

'''@author: Pranjal Verma'''

'''Why?:
	-creates variable-length, prefix-free, lossless compression encoding scheme for any 
	alphabet space with given weights for symbols.

	-Weights signify frequency of occurance of a symbol, and we derive an optimal encoding from
	these weights such that this encoding minimizes 'average encoding length' (AEL) of code.

	-AEL is the sum of bits used by each symbol weighted by it's weight (frequency).
'''

from heapq import heappop, heappush, heapify
from collections import defaultdict
from time import time

#sub-optimal func for generating Huffman encoder tree for given alphabet; O(nlogn)
#better solution exists using sorting and 2 queues (O(nlogn) + O(n) for queues)
#latter will still be O(nlogn) but will have better constants then given heap solution
#also, sorting can be further improved if domain of input is known!
def huffman(alphabet):

	#heap with keys as weights of symbols
	weightHeap, encoderTree = list(alphabet.items()), defaultdict(list)
	heapify(weightHeap) #O(n)

	#keeping track of roots of subtrees and finally getting root of entire tree
	#loop till all symbols are seen
	treeRoot = None
	while len(weightHeap) > 1:
		#pop 2 symbols with least weights
		a, b = heappop(weightHeap), heappop(weightHeap)

		#put them in tree with common parent node
		#left node of tree at index-0, indicating it's edge to parent is a bin-0
		#right node of tree at index-1, indicating it's edge to parent is a bin-1
		treeRoot = ''.join(a[1:]) + ''.join(b[1:])
		encoderTree[treeRoot].extend(b[1:])
		encoderTree[treeRoot].extend(a[1:])

		#push this new node onto heap with it's weight as the sum of weights of a & b
		heappush(weightHeap, (a[0] + b[0], treeRoot))

	#find depths of the computed encoder tree
	depth(encoderTree, treeRoot, 0)

#helper routine for finding depths using dfs; O(n)
def depth(tree, root, currDepth):
	global explored, depths

	#mark root as explored and recurse
	explored |= set([root])
	for node in tree[root]:
		if node not in explored:
			#keeping track of node's depth only if it's a symbol in given alphabet!
			#only 'node' for huffmanSmall/Quiz.txt
			if node in symbols:
				depths[node] = currDepth + 1

			depth(tree, node, currDepth + 1)

#init
if __name__ == '__main__':
	draft, alphabet = open('huffmanFinal.txt').read().splitlines(), {}
	explored, depths = set(), {}

	symbols = 'abcde' #for huffmanSmall/Quiz/Final.txt
	#symbols = range(1, int(draft[0]) + 1)
	for line, i in zip(draft[1:], symbols):
		alphabet[int(line)] = str(i)

	startTime = time()
	huffman(alphabet)
	endTime = time()

	print('Depths of various symbols:', depths)
	print('Max length of a codeword in the resulting Huffman code: ' + str(max(depths.values())))
	print('Min length of a codeword in the resulting Huffman code: ' + str(min(depths.values())))
	print('Time: ' + str(endTime - startTime))
