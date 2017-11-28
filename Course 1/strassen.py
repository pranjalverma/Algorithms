'''strassen.py: Divide & Conquer'''

'''Better than conventional matrix multiplication which is O(n^3).
Strassen's runs in O(n^log2(7)) = O(n^2.81)'''

import numpy as np

#recursive func for multiplying given matrix1 and matrix2
def strassen(matrix1, matrix2):
	n = matrix1.shape[0]
	if matrix1.size == 1 or matrix2.size == 1: #base case; trivially solved
		return matrix1 * matrix2
	else:
		#dividing matrix1 into blocks; reducing problem size
		a = matrix1[:n // 2, :n // 2]
		b = matrix1[:n // 2, n //2:]
		c = matrix1[n // 2:, :n // 2]
		d = matrix1[n // 2:, n // 2:]

		#dividing matrix2 into blocks; reducing problem size
		e = matrix2[:n // 2, :n // 2]
		f = matrix2[:n // 2, n //2:]
		g = matrix2[n // 2:, :n // 2]
		h = matrix2[n // 2:, n // 2:]

		#calculating 7 products according to strassen with trivial adds and subtracts
		#7 recursive calls
		prod1 = strassen(a, f - h)
		prod2 = strassen(a + b, h)
		prod3 = strassen(c + d, e)
		prod4 = strassen(d, g - e)
		prod5 = strassen(a + d, e + h)
		prod6 = strassen(b - d, g + h)
		prod7 = strassen(a - c, e + f)

		#adding matrix blocks together to form resultant matrix; O(n^2) 
		#matrix1 * matrix2
		return np.bmat([[prod5 + prod4 - prod2 + prod6, prod1 + prod2], 
						[prod3 + prod4, prod1 + prod5 - prod3 - prod7]])

#init
if __name__ == '__main__':
	print('For nxn matrices where n = even; ' + '\n' + 'Input format: ' + 'int1 int2 ...(row1); intx inty ...(row2); ...(rown)')
	print(strassen(np.matrix(input('Enter matrix1: ')), np.matrix(input('Enter matrix2: '))))
