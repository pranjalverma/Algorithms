'''mergesort.py: Divide & Conquer'''

'''Used to sort a given list of ints in O(nlogn) time, where n is num of ints'''

from time import time

#recursive func for mergesort
def mergesort(arr):
	length = len(arr)
	if length == 1: #base case; trivially solved
		return arr
	else:
		first_half = mergesort(arr[:length // 2]) #recursvely sorting first half of arr
		second_half = mergesort(arr[length // 2:]) #ecursvely sorting second half of arr
		return merge(first_half, second_half, length) #merge step in O(n)

#subfunc for merge step; O(n)
def merge(arr1, arr2, length):
	i = j = 0
	result, len1, len2 = [], len(arr1), len(arr2)
	
	for k in range(length):
		#break condition incase any subarr is scanned completely
		if i == len1:
			result.extend(arr2[j:])
			break
		elif j == len2:
			result.extend(arr1[i:])
			break

		#sorting in accending order, taking care of duplicates
		if arr1[i] < arr2[j]:
			result.append(arr1[i])
			i += 1
		elif arr2[j] < arr1[i]:
			result.append(arr2[j])
			j += 1
		else:
			result.append(arr1[i])
			i += 1
			result.append(arr2[j])
			j += 1
			k += 1

	return result

#init
if __name__ == '__main__':
	startTime = time()
	print(mergesort(list(map(int, open('mergesort.txt').read().splitlines()))))
	print('Time: ' + str(time() - startTime))
	#print(mergesort(list(map(int, input('Enter space-seperated array elements: ').split()))))
