'''heap.py: Data Structures'''

'''Once you understand that everything in python is "names & objects" instead of 
"variables & values" like say in C++!
https://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference :: 2nd ans
https://stackoverflow.com/questions/534375/passing-values-in-python :: vv imp'''

#basic min-Heap class
#raison d'être: repeated min/max calculations
class Heap:
	def __init__(self):
		'''putting an init value in heapList is crucial because it shifts ordering to 
		1-indexing in list, without which creating bubbleUp/bubbleDown funcs gets really 
		tricky, now self.length is just the last index of heapList!'''
		self.heapList = ['empty']
		self.length = 0

	#inserting new items
	def insert(self, k):
		self.heapList.append(k)
		self.length += 1
		self.bubbleUp(self.length)

	#heapifying from leaf to root; for insert operations in O(logn)
	def bubbleUp(self, i):
		#loop till we reach root!
		while i // 2 > 0:
			#swapping if parent is larger than child
			if self.heapList[i] < self.heapList[i // 2]:
				self.heapList[i // 2], self.heapList[i] = self.heapList[i], self.heapList[i // 2]
			i = i // 2

	#extracting root/minimum element from all n
	def extractMin(self):
		self.heapList[1], self.heapList[self.length] = self.heapList[self.length], self.heapList[1]
		self.length -= 1
		self.bubbleDown(1)
		return self.heapList.pop()

	#heapifying from root to leaves; for extract min operations in O(logn)
	def bubbleDown(self, i):
		#loop till we reach leaves (till i is last node that's a parent)
	    while (i * 2) <= self.length:
	        mc = self.minChild(i) #O(1)
	        #swap with min child if invariant violation
	        if self.heapList[i] > self.heapList[mc]:
	            self.heapList[i], self.heapList[mc] = self.heapList[mc], self.heapList[i]
	        i = mc

	#finding smallest child of given parent
	def minChild(self, i):
		#if only one child
	    if i * 2 + 1 > self.length:
	        return i * 2
	    else:
	    	#choosing min of both children
	        if self.heapList[i*2] < self.heapList[i*2 + 1]:
	            return i * 2
	        else:
	            return i * 2 + 1

#init
if __name__ == '__main__':
	heap = Heap()

	heap.insert(1)
	heap.insert(-1)
	heap.insert(2)
	heap.insert(10)
	heap.insert(471920)
	heap.insert(-1900)
	heap.insert(0)

	#effectively heapsort
	print(heap.heapList)
	for i in range(heap.length):
		print(heap.extractMin())
	print(heap.heapList)
