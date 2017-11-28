'''tsp1.py: Greedy Algorithm/NP-Complete'''

'''@author: Pranjal Verma'''

'''
	Running Time of O(n^2):
	The time is so because when exactly n/2 nodes are explored and n/2 nodes are unexplored,
	the outer while-loop and inner min() computation are both O(n), thus making the time O(n^2)
'''

from math import inf, sqrt

#greedy nearest-neighbour heuristic for the TSP problem, O(n^2) as above^
def tsp(cities):

	#init: unexplored maintains the set of nodes yet to be added to TSP tour
	unexplored, currNode, tour, cost = list(cities), 1, [1], 0
	unexplored.remove(currNode) #mark source as explored

	#construct TSP tour until all nodes are marked explored, O(n)
	while unexplored:

		#init 'current distance from current node in TSP tour to all unexplored nodes' to inf
		currDist = inf

		#find greedily, distance and identity of nearest neighbour to current node, O(n)
		#incase of a tie, the node with the lowest index is the nearest neighbour
		currDist, currNode = min((distance(currNode, nextNode), nextNode)
								for nextNode in unexplored)

		#mark this neighbour as explored
		unexplored.remove(currNode)

		#add this neighbour to TSP tour and add it's distance to TSP cost
		tour.append(currNode)
		cost += currDist

	#complete tour with one last hope back to source node from current node after all
	#nodes have been marked as explored
	tour.append(1)
	cost += distance(currNode, 1)

	#return final TSP tour cost
	return cost, tour

#func to compute euclidean distance b/w two cities, i -> j,  O(1) 
def distance(nodei, nodej):
	return sqrt((cities[nodej][0] - cities[nodei][0])**2 + (cities[nodej][1] - cities[nodei][1])**2)

#init: answer to tsp1.txt ~= 1203406
if __name__ == '__main__':
	cities, draft = {}, open('tsp1.txt').read().splitlines()

	for line in draft[1:]:
		city = list(map(float, line.split()))
		cities[int(city[0])] = city[1:]

	result = tsp(cities)
	print('TSP Cost: ' + str(result[0]))
	print('TSP Tour: ' + ' -> '.join(map(str, result[1])))
