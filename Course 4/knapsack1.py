'''knapsack1.py: Greedy Algorithm/Dynamic Programming/NP-Complete'''

'''@author: Pranjal Verma'''

'''Two Approximation Algorithms for the NP-Complete Knapsack Problem: greedy and dynamic'''

'''
	Correctness of Greedy Heuristic:
	Given algo is always gonna give a result that's at least 1/2 as good as the optimal result.
	More precisely, closeness of our result to the optimal result depends on how sizes of items
	are related to the knapsack capacity. See Tim Roughgarden's vid or check online for more.
'''

from operator import itemgetter
from time import time
from math import inf, floor

#run-time = O(n^2 * vMax) = O(n^3/errorFactor)
#user can specify an error factor upon which runtime and correctness both depend
#higher the error factor, more inaccurate the result, but faster the algo
def dynamicKnap(items, knapsackSize, errorFactor):

	#calc loss factor
	lossFactor = (errorFactor * max(items[item][0] for item in items)) / len(items)

	#creating new list of items with new floored values, all ints
	newItems = dict(items)
	for item in newItems:
		newItems[item][0] = floor(newItems[item][0] / lossFactor)

	#applying _knapByValue
	return _knapByValue(newItems, knapsackSize) * errorFactor

#sub-optimal O(n^2 * vMax) time algo for the Knapsack Problem;
#assuming values of items are ints; arbitrary weights and knapsack capacity
#runtime is polynomial only if vMax is polynomial in n
def _knapByValue(items, knapsackSize):
	
	#init
	cache, vMax = {}, int(max(items[item][0] for item in items))

	#using 0 items: (O(n*vMax))
	#weight = 0, if required value = 0
	#else, weight = inf 
	for value in range(len(items) * vMax + 1):
		if value == 0:
			cache[0, value] = 0
		else:
			cache[0, value] = inf

	#testing each possible value for every item, O(n^2 * vMax)
	for item in items:
		for value in range(len(items) * vMax + 1):

			#ensuring index correctness and applying recurrance, O(1)
			if value >= items[item][0]:
				cache[item, value] = min(cache[item - 1, value - int(items[item][0])] + items[item][1],
									cache[item - 1, value])
			else:
				cache[item, value] = min(items[item][1], cache[item - 1, value])

	#final scan through final n*vMax entries of cache, O(n*vMax)
	#returning highest value whose weight is valid wrt to the knapsack capicity
	for value in range(len(items) * vMax, -1, -1):
		if cache[len(items), value] <= knapsackSize:
			return float(value)

	raise Exception('Knapsack capacity too small!')

#blazingly fast greedy heuristic for the Knapsack Problem; exactly like schedule.py
#running time = O(nlogn); n = num of items
#Also, read correctness argument above^
def greedyKnap(items, knapsackSize):
	greedyOrder = []

	#init for greedy ordering: getting ratios, O(n)
	for item in items:
		greedyOrder.append((items[item][0], items[item][1], items[item][0] / items[item][1], item))

	'''
	side-note: sort() and sorted() maintain original ordering of unsorted list in case
	of ties among keys. First sort step sorts items so that items with larger values have 
	lower indices. Second sort step sorts this new ordering in decending order of greedy 
	scores, yet preserving the property that in case of ties in this step, items with larger 
	values will be considered first in result!
	'''
	greedyOrder.sort(key=itemgetter(0), reverse=True) #O(nlogn)
	greedyOrder.sort(key=itemgetter(2), reverse=True) #O(nlogn)

	#getting knapsack value and looted items, O(n)
	result = currentSize = 0
	loot = []
	for item in greedyOrder:
		if currentSize + item[1] <= knapsackSize:
			currentSize += item[1]
			result += item[0]
			loot.append(item[3])

	#comparing our result with the max value in items
	#and returning the winner of the two, O(n)
	vMax, vMaxItem = max((items[item][0], item) for item in items)
	if max(result, vMax) == result:
		return result, loot
	else:
		return vMax, vMaxItem

#init
if __name__ == '__main__':
	draft, items = open('knapsackTest.txt').read().splitlines(), {}

	knapsackSize, numItems = map(int, draft[0].split())
	for line, i in zip(draft[1:], range(1, numItems + 1)):
		items[i] = list(map(float, line.split()))

	startTime = time()
	loot = greedyKnap(items, knapsackSize)
	endTime = time()
	print('Greedy Knapsack solution: ' + str(loot[0]))
	print('Time: ' + str(endTime - startTime))

	startTime = time()
	print('Dynamic KnapByValue solution: ' + str(_knapByValue(items, knapsackSize)))
	print('Time: ' + str(time() - startTime))

	startTime = time()
	print('Dynamic heuristicKnap solution: ' + str(dynamicKnap(items, knapsackSize, 0.01)))
	print('Time: ' + str(time() - startTime))

	print('Greedy Loot: ' + str(loot[1]))
