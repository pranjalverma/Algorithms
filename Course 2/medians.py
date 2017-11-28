'''medians.py: Data Structures'''

'''len() costs only O(1), mad! 
https://stackoverflow.com/questions/1115313/cost-of-len-function'''

from heapq import heappush, heappop

#func for median maintenance; runs in O(logi) time for median among i numbers 
def medians(stream):
	#init
	heapHigh, heapLow, medians = [], [], []
	medians.append(stream[-1])
	if stream[-1] > stream[-2]:
		heappush(heapHigh, stream.pop())
		heappush(heapLow, -1 * stream.pop())
	else:
		heappush(heapLow, -1 * stream.pop())
		heappush(heapHigh, stream.pop())
	medians.append(-1 * heapLow[0])

	#chopping through stream of inputs one number at a time
	while stream:
		entry = stream.pop()

		#comparing with the two middle elements and maintaining heap invariant 
		if entry <= -1 * heapLow[0]:
			heappush(heapLow, -1 * entry)
		else:
			heappush(heapHigh, entry)

		#handling heaps imbalace
		if abs(len(heapHigh) - len(heapLow)) > 1:
			if len(heapLow) > len(heapHigh):
				heappush(heapHigh, -1 * heappop(heapLow))
			else:
				heappush(heapLow, -1 * heappop(heapHigh))

		#recording medians
		if len(heapLow) > len(heapHigh):
			medians.append(-1 * heapLow[0])
		elif len(heapHigh) > len(heapLow):
			medians.append(heapHigh[0])
		else:
			medians.append(-1 * heapLow[0])

	#last 4 digits of sum of all 10000 medians
	return sum(medians) % 10000

#init
if __name__ == '__main__':
	#stream = list(map(int, open('medians.txt').read().splitlines()))
	stream = [1, 2, 3, 4, 5]
	print(medians(list(reversed(stream)))) #direction of stream does matter in the sum!
