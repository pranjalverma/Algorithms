'''closestpair.py: Divide & Conquer/Geometric Algorithm'''

'''Finds the pair of points closest to each other in terms of Euclidean distance on a 2D plane
in O(nlogn) time'''

'''Side-note: this is where I discover that "import <module>" requires you to use don notation
i. e. "<module>.<func>" but with "from <module> import <func>" you can refer to the func by
name. Cool'''

from itertools import product
from operator import itemgetter
from math import hypot

#main recursive func for closest pair algorithm; O(nlogn)
def closestPair(graphX, graphY, n):
	half_n = n // 2

	#O(1) base case; trivially solved using brute force for small input size
	if n <= 3:
		bestDist, bestPair = 100000.0, []
		for i in range(n - 1):
			for j in range((i + 1) % n, n):
				temp = hypot(graphX[i][0] - graphX[j][0], graphX[i][1] - graphX[j][1])
				if temp < bestDist:
					bestDist, bestPair = temp, []
					bestPair.extend([graphX[i], graphX[j]])

		return (bestPair, bestDist)

	#main algo; 2 recursions and one conquer step that's O(n); same tree as mergesort
	else:
		#dividing graph in half for both kinds of sorts
		graphXleft, graphYleft = graphX[:half_n], graphY[:half_n]
		graphXright, graphYright = graphX[half_n:], graphY[half_n:]

		#getting three potential closest pairs
		pair1 = closestPair(graphXleft, graphYleft, len(graphXleft))
		pair2 = closestPair(graphXright, graphYright, len(graphXright))
		pair3 = closestSplitPair(graphX, graphY, n, min(pair1[1], pair2[1])) #O(n)

		#returning closest pair after sorting among potential pairs
		return sorted([pair1, pair2, pair3], key=itemgetter(1))[0]

#func for conquer step; O(n)
def closestSplitPair(graphX, graphY, n, curDist):
	#pivotX is the n/2th order statistic in X sort list of points
	pivotX, bestDist, bestPair = graphX[(n // 2) - 1][0], curDist, []

	#filtering step;
	#sub graph with Y sort containing points with X in curDist range from pivotX on both directions
	subGraphY = []
	for point in graphY:
		if pivotX - curDist <= point[0] <= pivotX + curDist:
			subGraphY.append(point)
	len_subGraphY = len(subGraphY)

	#checking filtered point; at max 7 other close points per point in outer loop iteration
	#sort of a greedy algorithm
	for i in range(len_subGraphY - 1):
		for j in range(1, min(7, len_subGraphY - i)):
			point1, point2 = subGraphY[i], subGraphY[i + j]
			dist = hypot(point1[0] - point2[0], point1[1] - point2[1])

			if dist <= bestDist:
				bestDist, bestPair = dist, []
				bestPair.extend([point1, point2])

	return (bestPair, bestDist)

#init
if __name__ == '__main__':
	graph = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)] #([(2, 3), (3, 4)], 1.4142135623730951)
	#graph = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10)] #([(2, 3), (5, 1)], 3.605551275463989)
	#graph = [(12, 30), (40, 50), (5, 1), (12, 10), (-5, -1)] #([(-5, -1), (5, 1)], 10.198039027185569)
	n = len(graph)
	print(closestPair(sorted(graph, key=itemgetter(0)), sorted(graph, key=itemgetter(1)), n))
