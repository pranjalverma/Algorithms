'''align.py: Dynamic Programming'''

'''@author: Pranjal Verma'''

'''
	Needleman-Wunsch Algorithm for scoring as (gap: -1/0, mismatch: -1/0, match: 1):

	Here, the lower the alignment score the larger the edit-distance'*', for this scoring system
	one wants a high score.
	'*': a string metric for measuring the difference between two sequences.
	Refer to 'Scoring systems' in the link below for more!
'''

'''
	Examples here:
	https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm (-1, -1, 1)
	http://biopython.org/DIST/docs/api/Bio.pairwise2-module.html (0, 0, 1)
'''

from collections import defaultdict

#O(mn) func for computing Needleman-Wunsch Score and alignment for a pair of strings
#cache(i, j) refer to the subproblem where:
#first i chars of strA are being aligned with first j chars of str B
def align(stringA, stringB, penalties):

	#init
	#cost of aligning a str with an empty-str is just (gap_cost * len(str))
	cache, lenA, lenB = {}, len(stringA), len(stringB)
	for i in range(lenA + 1):
		cache[(i, 0)] = i * penalties[0]
	for j in range(lenB + 1):
		cache[(0, j)] = j * penalties[0]

	cost_ij = 0
	for i in range(1, lenA + 1):
		for j in range(1, lenB + 1):

			#determining cost
			if stringA[i - 1] == stringB[j - 1]:
				cost_ij = penalties[2]
			else:
				cost_ij = penalties[1]

			#max() valid for say (-1, -1, 1) system. It may change if system is changed!
			#Eg- for (1, 1, 0), use min()
			cache[i, j] = max(cache[i - 1, j - 1] + cost_ij,
								cache[i - 1, j] + penalties[0],
								cache[i, j - 1] + penalties[0])

	alignment = reconstruct(cache, stringA, stringB, penalties)
	return cache[lenA, lenB], ''.join(reversed(alignment['A'])), ''.join(reversed(alignment['B']))

#O(mn) back-tracking algo to reconstruct alignment from given filled cache
def reconstruct(cache, stringA, stringB, penalties):
	alignment, i, j, cost_ij = defaultdict(list), len(stringA), len(stringB), 0

	while i > 0 or j > 0:
		if stringA[i - 1] == stringB[j - 1]:
			cost_ij = penalties[2]
		else:
			cost_ij = penalties[1]

		if i > 0 and j > 0 and cache[i, j] == cache[i - 1, j - 1] + cost_ij:
			alignment['A'].append(stringA[i - 1])
			alignment['B'].append(stringB[j - 1])
			i -= 1
			j -= 1
		elif i > 0 and cache[i, j] == cache[i - 1, j] + penalties[0]:
			alignment['A'].append(stringA[i - 1])
			alignment['B'].append('_')
			i -= 1
		else:
			alignment['A'].append('_')
			alignment['B'].append(stringB[j - 1])
			j -= 1

	return alignment

#init
if __name__ == '__main__':
	draft = open('align.txt').read().splitlines()
	#draft = open('align1.txt').read().splitlines()
	penalties = list(map(int, draft[0].split()))

	result = align(draft[1], draft[2], penalties)
	print(result[1])
	print(result[2])
	print('Score: ' + str(result[0]))
