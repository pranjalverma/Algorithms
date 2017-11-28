#TODO

from math import log
from random import getrandbits, choice

#num variables = num clauses
def papadimitriou(clauses, totalVars):
	numVars = len(totalVars)

	for freshStart in range(int(log(numVars, 2))):
		sat = {}
		for var in totalVars:
			sat[var] = bool(getrandbits(1))

		for i in range(2 * pow(numVars, 2)):
			checkSat = [(sat[clause[0]] if clause[0] > 0 else not sat[-1 * clause[0]])
						or (sat[clause[1]] if clause[1] > 0 else not sat[-1 * clause[1]])
						for clause in clauses.values()]

			if all(checkSat):
				return '1'
			else:
				faultyClause = checkSat.index(False) + 1 #get index of first faulty clause
				sat[choice(list(map(abs, clauses[faultyClause])))] ^= True #slick XOR to toggle bool

	return '0'

def reduceClauses(clauses):
	X, notX, newClauses = set(), set(), {}
	for clause in clauses.values():
		for var in clause:
			if var > 0:
				X |= set([var])
			else:
				notX |= set([-1 * var])

	trivialX = X ^ notX

	i, totalVars = 1, set()
	for clause in clauses.values():
		if not set(map(abs, clause)) & trivialX:
			newClauses[i] = clause
			totalVars |= set(map(abs, clause))
			i += 1

	print(len(newClauses), len(totalVars))
	return newClauses, totalVars

if __name__ == '__main__':
	indicatorBinStr = []

	for i in map(str, range(1, 6 + 1)):
		draft, clauses = open('2sat' + i + '.txt').read().splitlines(), {}

		for line, i in zip(draft[1:], range(1, int(draft[0]) + 1)):
			clauses[i] = tuple(map(int, line.split()))

		newClauses, totalVars = reduceClauses(clauses)
		indicatorBinStr.append(papadimitriou(newClauses, totalVars))
		print(''.join(indicatorBinStr))

	print(''.join(indicatorBinStr))
