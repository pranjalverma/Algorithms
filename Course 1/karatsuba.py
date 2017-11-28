'''karatsuba.py: Divide & Conquer'''

'''Provides a faster method for multiplying two n-digit ints than 
the grade school algo that runs in time O(n^2)'''

#recursive func for karatsuba; O(n^log2(3)) = O(n^1.59)
def karatsuba(x,y):
	if len(str(x)) == 1 or len(str(y)) == 1: #base case; trivially solved
		return x*y
	else:
		n = max(len(str(x)),len(str(y)))
		nby2 = n // 2
		
		#splitting nums
		a = x // 10**(nby2)
		b = x % 10**(nby2)
		c = y // 10**(nby2)
		d = y % 10**(nby2)
		
		#recursive calls for multiplying smaller ints
		ac = karatsuba(a,c)
		bd = karatsuba(b,d)
		ad_plus_bc = karatsuba(a+b,c+d) - ac - bd #gauss's trick
        
		return ac * 10**(2*nby2) + (ad_plus_bc * 10**nby2) + bd

#init
if __name__ == '__main__':
	x, y = int(input()), int(input())
	print(karatsuba(x, y))