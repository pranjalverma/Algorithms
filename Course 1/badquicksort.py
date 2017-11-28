'''badquicksort.py: Divide & Conquer'''

'''Sorting algorithm'''

'''So this is where I discovered this amazing thing: 
https://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference
'''

'''time.time(): this calculates the real time though (including time used by other programs) so 
it will seem to take more time when your computer is busy doing other stuff'''

from time import process_time

#recursive func for quicksort; runs in O(n^2) time (baaad!)
def qsort(arr, l, r):
    if l < r: #as long as there's as least one element in arr
        pivot = partition(arr, l, r) #Conquer; O(n)

        #Divide
        qsort(arr, l, pivot - 1)
        qsort(arr, pivot + 1, r)

    return arr

#sub-routine for partitioning around pivot; O(n)
def partition(arr, l, r):
    pivot, i = arr[l], l #choosing pivot naively 

    for j in range(l + 1, r + 1):
        if arr[j] < pivot:
            i += 1
            arr[j], arr[i] = arr[i], arr[j] # Cool ass python swapping
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
