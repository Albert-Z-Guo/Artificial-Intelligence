HYPOTHESIS_SPACE = [True, False]

def ask(var, value, evidence, bn):
	# distribution over var, initially empty
	distri = {}

	# for each value of var
	for x in HYPOTHESIS_SPACE:
		# extend evidence with var: var = x
		e = evidence.copy()
		e.update({var: x})
		distri[x] = enumerate_all(bn.variables, e)

	return distri[value] / sum(distri.values())

def enumerate_all(variables, evidence):
	if len(variables) == 0: return 1.0

	# Y is the first variable in list
	Y = variables[0]

	# if Y has value y in e
	for y in HYPOTHESIS_SPACE:
		if Y.name in evidence and y == evidence[Y.name]:
			return Y.probability(y, evidence) * enumerate_all(variables[1:], evidence)

	# if Y does not have value y in e
	else:
		sum = 0
		for y in HYPOTHESIS_SPACE:
			# extend evidence with Y = y
			e = evidence.copy()
			e.update({Y.name: y})
			sum += Y.probability(y, e) * enumerate_all(variables[1:], e)
		return sum
