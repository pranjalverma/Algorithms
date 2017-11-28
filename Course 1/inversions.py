'''inversions.py: Divide & Conquer'''

'''Counts num of inversions in a given list of ints in O(nlogn) time;
piggybacks on the principle of mergesort'''

'''Inversions is a pair of ints arr[i[ and arr[j] where arr[i] > arr[j] for
i < j, in given list arr'''

#recursive func for counting inversions
def countInvs(arr):
	length = len(arr)

	if length == 1: #base case; trivially solved
		return (arr, 0)
	else:
		first_half, left_count = countInvs(arr[:length // 2]) #left inversions
		second_half, right_count = countInvs(arr[length // 2:]) #right inversions
		sorted_arr, split_count = countSplitInvs(first_half, second_half, length) #split inversions

		return sorted_arr, left_count + right_count + split_count

#sub func for counting split inversions; O(n)
def countSplitInvs(first_half, second_half, length):
	i = j = inv_count = 0
	len1, len2, sorted_arr = len(first_half), len(second_half), []

	for k in range(length):
		#break conditions; incase one subarr is scanned completely
		if i == len1:
			sorted_arr.extend(second_half[j:])
			break
		elif j == len2:
			sorted_arr.extend(first_half[i:])
			break

		#merging in accending order to produce sorted arr
		if first_half[i] < second_half[j]:
			sorted_arr.append(first_half[i])
			i += 1
		elif second_half[j] < first_half[i]:
			sorted_arr.append(second_half[j])
			inv_count += len1 - i #keeping count of inversions
			j += 1

	return (sorted_arr, inv_count)

#init
if __name__ == '__main__':
	print('Sorted array, no. of inversions: ' + str(countInvs(list(map(int, input('Enter space-seperated array elements: ').split())))))

'''Can be used in match-making of two ranked lists. Eg- can used by online stores to 
find a sense of similarity between customers so as to provide better recommendations'''
