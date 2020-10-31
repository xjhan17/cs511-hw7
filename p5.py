from z3 import *
import sys
import numpy as np
import ast
import json

# get input from either input .txt file or script
# format in input file: [[objective terms], [subjective terms], ...]
# e.g: [[[1, [[0, 1]]], [1, [[0, 2]]]], [[1, [[0, 1], [1, 2]]], [2, [[0, 2]]], [-3, [[0, 1]]], [-1, []]], [[-1, [[0, 1], [1, 2]]], [-2, [[0, 2]]], [3, [[0, 1]]], [1, []]]]
# format in script: same as described in hw 7 p5
# e.g: [ \
#      [ [1, [[0, 1]]], [1, [[0, 2]]]], \
#      [ [1, [[0, 1], [1, 2]]], [2, [[0, 2]]], [-3, [[0, 1]]], [-1, []]], \
#      [ [-1, [[0, 1], [1, 2]]], [-2, [[0, 2]]], [3, [[0, 1]]], [1, []]] \
#      ]


if len(sys.argv) > 1:
    # file = open(sys.argv[1], 'r')
    # line = file.readline()
    # inputlist.ast.literal_eval(line)
	file = sys.argv[1]
	with open(file, 'r') as fi:
		inputline = fi.readline()
		inputlist = ast.literal_eval(inputline)
else:
    inputlist = [ \
                [ [1, [[0, 1]]], [1, [[0, 2]]]], \
     	        [ [1, [[0, 1], [1, 2]]], [2, [[0, 2]]], [-3, [[0, 1]]], [-1, []]], \
     	        [ [-1, [[0, 1], [1, 2]]], [-2, [[0, 2]]], [3, [[0, 1]]], [1, []]] \
                ]

def main():
    s = Optimize()
    variables = []
    count = []
    function = objectiveFunction(variables, count)
    constraints = PBConstraint(variables, count)
    s.add(constraints)
    s.minimize(function)
    if s.check() == sat:
        print('True: PB-constraints are satisfiable, with (0,1) assignments as below: ')
        model = s.model()
        for a in model:
            print('variable: ' + str(a) + ' value assignment: ' + str(model[a]))
    else:
        print('False: PB-constraints are NOT satisfiable')



def objectiveFunction(variables, count):
    function = 0
    for terms in inputlist[0]:
        subFunction = terms[0]
        for lists in terms[1]:
            variable = Int('x%s' % lists[1]) if lists[0] == 0 else Int('-x%s' % lists[1])
            variables.append(variable) if variable not in variables else variables
            count.append(lists[1]) if lists[1] not in count else count
            subFunction *= variable
        function += subFunction
    return function

def PBConstraint(variables, count):
    constraints = []
    for i in range(1, len(inputlist)):
        constraint = -1
        for currentList in inputlist[i]:
            subConstraint = currentList[0]
            for lists in currentList[1]:
                variable = Int('x%s' % lists[1]) if lists[0] == 0 else Int('-x%s' % lists[1])
                variables.append(variable) if variable not in variables else variables
                count.append(lists[1]) if lists[1] not in count else count
                subConstraint = subConstraint * variable
            constraint = subConstraint if constraint == -1 else constraint + subConstraint
        constraints.append(constraint<=0)
    
    # setting up constraints: 
    # 1. variables can only assume values 0 or 1
    # 2. negation of x, Bar x = 1-x
    for i in count:
        constraints.append(Or(Int('x'+str(i)) == 1, Int('x'+str(i)) == 0))
        constraints.append(Or(Int('-x' + str(i)) == 1, Int('-x' + str(i)) == 0))
        constraints.append(Int('x'+str(i)) + Int('-x' + str(i)) == 1)
    return constraints



if __name__== "__main__":
    main()