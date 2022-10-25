# Cellular Automaton
# based on rule 110
# [version], [release date]

version = 2.71
#added mutation of rules and cells
import random

def cellularAutomaton(rulenum = 110, wraparound = True, columns = 120, mutation = True):

    def ruleMutate(d):
        if not mutation:
            return
        if random.randrange(1,50) == random.randrange(1,50):
            d[random.choice(list(d.keys()))] = random.choice([0,1])
        
    def mutate(lis):
        if not mutation:
            return
        if random.randrange(1,10) == random.randrange(1,10):
            for x in range(random.randrange(len(lis))):
                if random.choice([True, False]):
                    lis[random.randrange(len(lis))] = random.choice([0,1])
                     
    vname = f"Cellular Automaton v{version}\nRule {rulenum}\n{columns} Columns, Wraparound: {wraparound}"
    print(vname)

    caseKeys = [int(x) for x in bin(rulenum).replace('0b', '')]

    while len(caseKeys) < 8:
        caseKeys = [0] + caseKeys
        
    genMatrix = []  # two dimension matrix of generations

    # 0 = off
    # 1 = on

    # numGens = 200  # generations/rows to compute

    # rules reference top 3 cells (genMatrix[gen-1][ind-1,ind, ind+1])
    rules = {0b111: 0, 0b110: 0, 0b101: 0, 0b100: 0, 0b011: 0, 0b010: 0, 0b001: 0, 0b000: 0}


    for c in range(len(rules)):
        rules[list(rules.keys())[c]] = caseKeys[c]

    def findRule(d):
        s = '0b'
        for key in d:
            s += str(d[key])
        return int(s,2)

    # create the first generation and add it to genMatrix
    firstGen = [0 for x in range(columns)]
    firstGen[columns-1] = 1
    genMatrix.append(firstGen)

    outcells = [firstGen[-1], firstGen[0]] #the values of the cell outside the frame (wrap around)

    def computeGen(prev, rulDict, out):
        '''computes a new generation based on the rules and previous row
           returns a list of the same size as "prev"
           prev  --> 1 dimensional list
           rulDict --> dictionary
           out  --> values of the cells immediately out of the frame'''
        
        #create fresh generation
        new = [0 for x in range(len(prev))]
        for r in range(0, len(prev)):
            # get the top 3
            top3 = [0, prev[r], 0]

            # before
            if r-1 < 0:
                # referencing out of range
                top3[0] = out[0]
            else:
                # all good
                top3[0] = prev[r-1]
                
            #after
            if r+1 > len(prev)-1:
                # referencing out of range
                top3[2] = out[1]
            else:
                # all good
                top3[2] = prev[r+1]

            # currently the top 3 cells are in a list
            # we need to convert them to a combined 3 digit integer
            # then to int as binary
            # then get the value of the current cell out of the rules
            
            # to do that we first convert each item in top3 to string
            # and then join them
            # and do int(_, 2) bc we want it treated as base 2
            combinedNum = ''.join([str(i) for i in top3])
            intNum = int(combinedNum, 2)
            new[r] = rulDict[intNum]
        
        return new

    def convertRow(lis):
        ''' prints a list in terms of ' ' and 'X'''
        rs = ''
        for digit in lis:
            match digit:
                case 0:
                    rs += ' '
                case 1:
                    rs += 'X'
        return rs

    generation = 1
    while True: #genMatrix[generation-1][0] != 1:
        # get the previous generation
        previous = genMatrix[generation-1]
        
        # compute new generation
        newGen = computeGen(previous, rules, outcells )
        mutate(newGen)
        outcells = [newGen[-1], newGen[0]] # refresh outcells

        # print the row
        print(convertRow(previous), end = f' |{generation}|{findRule(rules)}\n')
        # append generation to genMatrix
        genMatrix.append(newGen)
        generation += 1
        ruleMutate(rules)

        if not wraparound:
            # if not wraparound end sequence as soon as it goes out of frame
            if previous[1] == 1:
                print()
                print('out of frame')
                return
if __name__ == '__main__': cellularAutomaton(int(input('Rule (int): ')), 't' == input('Wraparound (T/F): ').lower()[0], int(input('Columns (int): ')), 't' == input('Mutation (True/False): ').lower())
                                           

