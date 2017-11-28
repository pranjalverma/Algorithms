'''dselect.py: Divide & Conquer'''

'''Deterministic version of quickselect; finds the ith order statistic in a given list of 
unsorted, unique ints; ith order statistic is the ith smallest element in the sorted version 
of the given list. Runtime: O(n)'''

'''slicing beyond end-of-list endex doesn't raise error, hey-ho'''

from time import process_time

#main recursive func for deterministic quickselect; O(n)
def dselect(arr, l, r, i):
	if l < r:
		#finding pivot using median of medians approach
		medians = createMedianList(arr, l, r)
		pivot = dselect(medians, 0, len(medians) - 1, len(medians) // 2)

		pivot = partition(arr, l, r, pivot)
		if pivot + 1 == i:
			return arr[pivot]
		elif pivot + 1 > i:
			return dselect(arr, l, pivot - 1, i)
		else:
			return dselect(arr, pivot + 1, r, i)

	return arr[l]

#sub-routine for partitioning around pivot; O(n)
def partition(arr, l, r, pivot):
	pivotIndex, i = arr.index(pivot), l
	arr[l], arr[pivotIndex] = arr[pivotIndex], arr[l]

	for j in range(l + 1, r + 1):
		if arr[j] < arr[l]:
			i += 1
			arr[i], arr[j] = arr[j], arr[i]
	arr[l], arr[i] = arr[i], arr[l]

	return i

#fuck this shit, it's sloppy but at least it fucking works now jesus fucking christ
'''sub-routine for creating list of medians by dividing arr into groups of 5, sorting
trivially and returning their respective medians in a list; O(n)'''
#take care not to return empty lists here!
#divising a formula in terms of `l` and `r` for the slicing and range is fucking tough
def createMedianList(arr, l, r):
	medians, tempArr = [], arr[l:r + 1]
	for i in range(0, len(tempArr), 5):
		temp = sorted(tempArr[i:i + 5])
		medians.append(temp[len(temp) // 2])

	return medians

#init
if __name__ == '__main__':
	startTime = process_time()

	arr = [5, 2, 4, 3, 1, -1]
	print('Given list: ' + str(arr))
	#arr = list(map(int, open('select.txt').read().splitlines()))
	print(dselect(arr, 0, len(arr) - 1, int(input('Which order statistic to find? '))))

	print(process_time() - startTime)

