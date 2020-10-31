from z3 import *
import sys
import numpy as np
import ast




if len(sys.argv) > 1:
	file = sys.argv[1]
	with open(file, 'r') as fi:
		inputline = fi.readline()
		L = ast.literal_eval(line)
else:
	L = [ \
        [ [1, [[0, 1]]], [1, [[0, 2]]]], \
     	[[1, [[0, 1], [1, 2]]], [2, [[0, 2]]], [-3, [[0, 1]]], [-1, []]], \
     	[[-1, [[0, 1], [1, 2]]], [-2, [[0, 2]]], [3, [[0, 1]]], [1, []]] \
        ]


variables = []
count = []

def objectiveFunction():
    formula = -1
    for term in L[0]:
        sub_formula = term[0]
        for var_lst in term[1]:
            if var_lst[0] == 0:
                var = Int('x%s' % var_lst[1])
            else:
                var = Int('-x%s' % var_lst[1])
            if var not in variables:
                variables.append(var)
            if var_lst[1] not in count:
                count.append(var_lst[1])
            sub_formula *= var
        if formula == -1:
            formula = sub_formula
        else:
            formula += sub_formula
    return formula

def PBConstraint():
    constraints = []
    for j in range(1, len(L)):
        constraint = -1
        for cur_lst in L[j]:
            sub_constraint = cur_lst[0]
            for var_lst in cur_lst[1]:
                if var_lst[0] == 0:
                    var = Int('x%s' % var_lst[1])
                else:
                    var = Int('-x%s' % var_lst[1])
                if var not in variables:
                    variables.append(var)
                if var_lst[1] not in count:
                    count.append(var_lst[1])
                sub_constraint *= var
            if constraint == -1:
                constraint = sub_constraint
            else:
                constraint += sub_constraint
        constraints.append(constraint <= 0)
    
    # setting up constraints: 
    # 1. variables can only assume values 0 or 1
    # 2. negation of x, Bar x = 1-x
    for i in count:
        variableConstraint = Or(Int('x'+str(i)) == 1, Int('x'+str(i)) == 0)
        constraints.append(variableConstraint)
        variableConstraint = Or(Int('-x' + str(i)) == 1, Int('-x' + str(i)) == 0)
        constraints.append(variableConstraint)

        variableConstraint = Int('x'+str(i)) + Int('-x' + str(i)) == 1
        constraints.append(variableConstraint)
    return constraints


def main():
    s = Optimize()
    formula = objectiveFunction()
    constraints = PBConstraint()
    s.add(constraints)
    s.minimize(formula)
    if s.check() == unsat:
        print('false')
    else:
        print('true')
        m = s.model()
        sorted_model = sorted([(d, m[d]) for d in m], key=lambda x: str(x))
        print(sorted_model)


if __name__== "__main__":
    main()