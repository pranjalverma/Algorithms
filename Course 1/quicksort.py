'''quicksort.py: Divide & Conquer'''

'''Sorting algorithm'''

'''has amazing mathematical run-time proof btw'''

from time import process_time
from random import randrange

#recursive func for quicksort; runs in O(nlogn) time (goood!)
def qsort(arr, l, r):
    if l < r: #as long as there's as least one element in arr
        pivot = partition(arr, l, r) #Conquer; O(n)

        #Divide
        qsort(arr, l, pivot - 1)
        qsort(arr, pivot + 1, r)

    return arr

#sub-routine for partitioning around pivot; O(n)
def partition(arr, l, r):
    #choosing pivot randomly
    '''the pivot in Quicksort should be chosen from the elements of the 
    sub-array being partitioned'''
    pivot, i = randrange(l, r + 1), l
    arr[l], arr[pivot] = arr[pivot], arr[l]

    for j in range(l + 1, r + 1):
        if arr[j] < arr[l]:
            i += 1
            arr[j], arr[i] = arr[i], arr[j] # Cool python swapping
    arr[i], arr[l], = arr[l], arr[i]

    #position of pivot in partitioned arr
    return i

#init
if __name__ == '__main__':
	startTime = process_time()

	#arr= [5, 4, 3, 2, 1, 1, -1]
	arr = list(map(int, open('quicksort.txt').read().splitlines()))
	print(qsort(arr, 0, len(arr) - 1))

	print(process_time() - startTime)
