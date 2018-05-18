'''
knapsack.py: Dynamic Programming
@author: Pranjal Verma
'''

'''defaultdict:
	defaultdict is faster than {} for larger data sets with more homogenous key sets
	like here in knapsackBig.
'''

from collections import defaultdict
from sys import setrecursionlimit
from time import time

#for 'knapsackBig.txt'
setrecursionlimit(20000)

#O(nW) time, iterative func for a general knapsack problem
#n = num of Items and W = knapsack capacity
#kinda analogous to MWIS problem; items aranged in a path graph!
def knapsack(items, knapsackSize):
	cache = defaultdict(list)
	cache[0] = [0] * (knapsackSize + 1)

	#for first 'item' num of items allowed (prefixes of items!)
	for item in items:

		#for 'size' of knapsack allowed (prefixes of knapsack size!)

		#here the assumption that "W and w_i's are ints" can be seen used
		#this for-loop won't make sense in this algo if they were not ints!
		for size in range(knapsackSize + 1):
			if size >= items[item][1]:
				cache[item].append(max(cache[item - 1][size], 
					cache[item - 1][size - int(items[item][1])] + items[item][0]))
			else:
				cache[item].append(cache[item - 1][size])

	#returning optimal solution for main problem
	return cache[numItems][knapsackSize]

#O(nW) run-time with better constants and O(W) space-complexity!
#Using only one list of size O(W) to generate entire cache
#Not useful if reconstruction is needed as a post-processing step
def knapsackOptimised(items, knapsackSize):
	cache = [0] * (knapsackSize + 1)
	for item in items:
		for size in range(knapsackSize, 0, -1):
			if items[item][1] <= size:
				#single list is both ith and (i-1)th column of cache!
				cache[size] = max(cache[size - int(items[item][1])] + items[item][0],
					cache[size])
	return cache[knapsackSize]

#only version that works with both big and small data sets.
#only successful algo for big data set, but slowest for small data set?!
def knapsackBig(items, knapsackSize):
	cache = {}

	#main recursive func to help fill cache
	def bigHelper(item, size):
		#hashing tuples for this if-condition
		if (item, size) not in cache:
			if item == 0:
				cache[item, size] = 0
			elif items[item][1] > size:
				cache[item, size] = bigHelper(item - 1, size)
			else:
				cache[item, size] = max(bigHelper(item - 1, size),
					bigHelper(item - 1, size - items[item][1]) + items[item][0])
		return cache[item, size]

	return bigHelper(len(items), knapsackSize), reconstructBig(cache, items, knapsackSize)

#reverse-pass reconstruction step for getting the actual set of items in optimal solution
#similar algorithm for knapsack(), not implemented here
def reconstructBig(cache, items, knapsackSize):
	loot, item, size = set(), len(items), knapsackSize

	#until knapsack is full
	while cache[item, size] != 0:
		if cache[item, size] != cache[item - 1, size]:
			loot |= set([item])
			size -= int(items[item][1])
		item -= 1

	return loot

#init: answer for 'knapsackSmall.txt' = 8, {3, 4}
if __name__ == '__main__':
	draft, items = open('knapsack.txt').read().splitlines(), {}
	knapsackSize, numItems = map(int, draft[0].split())

	for line, i in zip(draft[1:], range(1, numItems + 1)):
		items[i] = list(map(float, line.split()))

	startTime = time()
	print('Knapsack solution: ' + str(knapsack(items, knapsackSize)))
	print('Time: ' + str(time() - startTime))

	startTime = time()
	print('Optimised Knapsack solution: ' + str(knapsackOptimised(items, knapsackSize)))
	print('Time: ' + str(time() - startTime))

	startTime = time()
	loot = knapsackBig(items, knapsackSize)
	print('Big Knapsack solution: ' + str(loot[0]))
	print('Time: ' + str(time() - startTime))

	print('Loot: ' + str(loot[1]))
