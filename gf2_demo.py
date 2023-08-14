import gf2

print(f'Starting GF2 demo.')
gf = gf2.Init(285)
print(gf)

print(f'Demonstrate multiplication and division in this field:')
a = 2
b = 5
result = gf2.Multiply(a,b,gf)
print(f'{a} x {b} = {result}')
print(f'{result} / {b} = {gf2.Divide(result,b,gf)}')
a = 200
b = 255
result = gf2.Multiply(a,b,gf)
print(f'{a} x {b} = {result}')
print(f'{result} / {b} = {gf2.Divide(result,b,gf)}')

print(f'Demonstrate convolution in this field:')
poly1 = [1, 4]
poly2 = [1, 8]
result = gf2.Convolve(poly1, poly2, gf)
print(f'{poly1} * {poly2} = {result}')
poly1 = [1, 200]
poly2 = [4, 100]
result = gf2.Convolve(poly1, poly2, gf)
print(f'{poly1} * {poly2} = {result}')

print(f'Demonstrate reciprocal in this field:')
a = 30
inverse = gf2.Reciprocal(a, gf)
print(f'a = {a}, 1 / a = {inverse}, a x {inverse} = {gf2.Multiply(a,inverse,gf)}')
print(f'log({a}) = {int(gf["Index"][a])}, log({inverse}) = {int(gf["Index"][inverse])}')

print(f'Search for maximal generator polynomials.')
found = 0
generator = (1<<8) + 1
while found == 0:
	gf = gf2.Init(generator)
	if gf['CycleCount'] == 1:
		print(f'Found generator polynomial {generator}! ', end='')
		factor_tap = 65536
		exponent = 16
		while factor_tap > 0:
			if generator & factor_tap:
				if factor_tap < (generator >> 1):
					print(f' + ', end='')
				if exponent > 1:
					print(f'x^{exponent}', end='')
				elif exponent == 1:
					print('x', end='')
				elif exponent == 0:
					print('1', end='')
			factor_tap >>= 1
			exponent -= 1
		print(' ')
		found += 1
	generator += 2
print(f'Found {found} maximal generator polynomials.')
