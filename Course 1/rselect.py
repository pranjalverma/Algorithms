'''rselect.py: Divide & Conquer'''

'''Finds the ith order statistic in a given list of unsorted, unique ints; ith order statistic 
is the ith smallest element in the sorted version of the given list. Runtime: O(n)'''

'''wow: https://stackoverflow.com/questions/5131538/slicing-a-list-in-python-without-generating-a-copy'''

from random import randrange
from time import process_time

#recursive func for rselect; O(n); combination of Binary Search and randomised Quicksort!
def rselect(arr, l, r, i):
	if l < r:
		pivot = partition(arr, l, r)

		#because pivot element is now in correct order statistic position in arr
		if pivot + 1 == i:
			return arr[pivot]
		elif pivot + 1 > i:
			return rselect(arr, l, pivot - 1, i)
		else:
			'''i = i - pivot - 1 only when actually passing new lists, changing the new list's 
			indices, but here indices are tracked using 'l' and 'r' so 'i' remains 'i'.'''
			return rselect(arr, pivot + 1, r, i) #omg

	return arr[l]

#sub-routine for partitioning around pivot; O(n)
def partition(arr, l, r):
	#randomly choosing pivot; for good balance
	pivot, i = randrange(l, r + 1), l
	arr[l], arr[pivot] = arr[pivot], arr[l]

	for j in range(l + 1, r + 1):
		if arr[j] < arr[l]:
			i += 1
			arr[i], arr[j] = arr[j], arr[i]
	arr[i], arr[l] = arr[l], arr[i]

	#pivot index in arr
	return i

#init
if __name__ == '__main__':
	startTime = process_time()

	#arr = list(map(int, open('select.txt').read().splitlines()))
	arr = [5, 3, 4, 1, 2, -1]
	print('Given list: ' + str(arr))
	print(rselect(arr, 0, len(arr) - 1, int(input('Which order statistic to find? '))))

	print(process_time() - startTime)
