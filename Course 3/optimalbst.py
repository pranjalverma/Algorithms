'''optimalbst.py: Dynamic Programming'''

'''@author: Pranjal Verma'''

'''
	Optimal BST (OBST):
	A BST that provides better look ups on average than a balanced BST, provided frequecies
	of various look ups is given. May or may not be balanced.
'''

'''
	Average/Weighted Search Time (WST) of Optimal BST:
	Search time for a given node in an BST refers to the number of nodes encountered in the
	path taken to find the given node, which also includes given node.
	WST of a OBST then refers to the weighted sum of the search times of every node in the tree,
	each search time weighted by a given frequency or weight of that node.
'''

from collections import defaultdict

#naïve On^3) DP algo for computing WST of optimal BST of n nodes!
def computeOBST(alphabet):
	cache, numNodes = {}, len(alphabet)

	#s = (j - i)
	#i starts from 1 because node numbering is 1-indexed
	#and i ends at i=(n-s) because here j=i + s is now the last nth node!
	for s in range(numNodes):
		for i in range(1, numNodes - s + 1):
			#init before recurrence
			#two cases where 1st index > 2nd index doesn't make sense:
			#such a case refers to an optimal bst having nodes numbered between
			#(a, b) where a > b, implying the bst is empty, thus it's WST = 0
			weightSum = sum([alphabet[k] for k in range(i, i + s + 1)])
			cache[i, i - 1] = cache[i + s + 1, i + s] = 0

			#main recurrence, where significant subproblems are brute-forced and cached!
			cache[i, i + s] = weightSum + min([cache[i, root - 1] + cache[root + 1, i + s]
									for root in range(i, i + s + 1)])

	#returning WST of the optimal bst with having nodes numbered b/w 1 and n; i.e. all nodes! 
	return cache[1, numNodes], constructOBST(cache, alphabet)

def constructOBST(cache, alphabet):
	tree, i, j = defaultdict(list), 1, len(alphabet)
	#TODO

#init
if __name__ == '__main__':
	draft, alphabet = open('optimalbstFinal.txt').read().splitlines(), {}

	for line, i in zip(draft[1:], '1234567'):
		alphabet[int(i)] = int(line)

	print('Alphabet: ' + str(alphabet))

	obst = computeOBST(alphabet)
	print('Weighted Search Time of this tree: ' + str(obst[0]))
