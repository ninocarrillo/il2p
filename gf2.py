import numpy

def Multiply(a, b, gf):
	result = 0
	if a == 0 | b == 0:
		return result
	a = int(gf['Index'][a])
	b = int(gf['Index'][b])
	result = a + b
	while result > (gf['Order'] - 2):
		result = result - (gf['Order'] - 1)
	return int(gf['Table'][result])

def Divide(a, b, gf):
	if b == 0:
		return 0xFFFF
	if a == 0:
		return 0
	a = int(gf['Index'][a])
	b = int(gf['Index'][b])
	a = a - b
	while a < 0:
		a += (gf['Order'] - 1)
	return int(gf['Table'][a])

def Convolve(poly1, poly2, gf):
	result_order = len(poly1) + len(poly2) - 1
	result = numpy.zeros(result_order)
	index1 = 0
	while index1 < len(poly1):
		index2 = 0
		while index2 < len(poly2):
			result[index1 + index2] = int(result[index1 + index2]) ^ int(Multiply(poly1[index1], poly2[index2], gf))
			index2 += 1
		index1 += 1
	return result

def Reciprocal(a, gf):
	return int(gf['Table'][(gf['Order'] - 1) - int(gf['Index'][a])])

def Init(genpoly):
	this = {}
	this['GenPoly'] = genpoly

	# Reduce the generating polynomial to determine the field power.
	# The number of elements in the field is called the order of the field.
	# Field order = 2 ^ Power.
	this['Power'] = 0
	while (genpoly > 1):
		genpoly >>= 1
		this['Power'] += 1

	this['Order'] = 1 << this['Power']

	# Keep track of how many times the field repeats, for maximal determination.
	# CycleCount will equal 1 after initialization if field is maximal.
	this['CycleCount'] = 0

	this['Table'] = numpy.zeros(this['Order'])
	this['Index'] = numpy.zeros(this['Order'])

	## Generate field table and index.
	# Start with element a^0, which is equal to 1.
	lfsr = 1
	index = this['Order'] - 2
	while index >= 0:
		## Step the lfsr once.
		feedback_bit = lfsr & 1
		lfsr >>= 1
		if feedback_bit == 1:
			lfsr = lfsr ^ (this['GenPoly'] >> 1)
		if lfsr == 1:
			this['CycleCount'] += 1
		# Save the field value and its index.
		this['Table'][index] = lfsr
		if this['Index'][lfsr] == 0:
			this['Index'][lfsr] = index
		else:
			this['CycleCount'] += 1
		index -= 1

	return this
