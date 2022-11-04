import nonogame

from numpy import random
import numpy as np

def printSol(sol, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints
    steps_array = []
    steps = nonogame.Game(nLines,  nColumns, sol.points).board
    for index, solution in enumerate(steps):
        num = np.array(solution).flatten().tolist()
        for index, a in enumerate(num):
            if a == True: num[index] = 1
            if a == False: num[index] = 0
            if a == None: num[index] = 0
        steps_array.append(num)
        
    return steps_array

def readRulesFile(fileName):
    with open(fileName) as rulesFile:
        readingLines = True
        lines   = []
        columns = []

        for fileLine in rulesFile:
            if(fileLine == '-\n'):
                readingLines = False
                continue

            rulesInFileLine = [[int(rule) for rule in fileLine.split()]]
            if(readingLines):
                lines   += rulesInFileLine
            else:
                columns += rulesInFileLine

    return nonogame.Rules(lines=lines, columns=columns)

def createConstraints(rules, nPopulation):
    nLines   = len(rules.lines)
    nColumns = len(rules.columns)
    nPoints  = 0

    # Count total number of points
    for line in rules.lines:
        for rule in line:
            nPoints += rule

    return (rules, nLines, nColumns, nPoints, nPopulation)

def fitness(sol, constraints):
    rules, nLines, nColumns, nPoints, nPopulation = constraints

    # Count how many rules it is following
    count = 0
    game  = nonogame.Game(nLines, nColumns, sol)
    board = sol

    # Count in lines in ascending order
    for lineIndex in range(nLines):
        rulesQtt = len(rules.lines[lineIndex])

        columnIndex = 0
        ruleIndex   = 0

        while columnIndex < nColumns or ruleIndex < rulesQtt:
            countSegment = 0
            currRule     = rules.lines[lineIndex][ruleIndex] if ruleIndex < rulesQtt else 0

            while columnIndex < nColumns and not board[lineIndex*nColumns + columnIndex]:
                columnIndex += 1

            while columnIndex < nColumns and board[lineIndex*nColumns + columnIndex]:
                countSegment += 1
                columnIndex += 1

            count -= abs(countSegment - currRule)
            ruleIndex += 1

    # Count in columns in ascending order
    for columnIndex in range(nColumns):
        rulesQtt = len(rules.columns[columnIndex])

        lineIndex = 0
        ruleIndex = 0

        while lineIndex < nLines or ruleIndex < rulesQtt:
            countSegment = 0
            currRule     = rules.columns[columnIndex][ruleIndex] if ruleIndex < rulesQtt else 0

            while lineIndex < nLines and not board[lineIndex*nColumns + columnIndex]:
                lineIndex += 1

            while lineIndex < nLines and board[lineIndex*nColumns + columnIndex]:
                countSegment += 1
                lineIndex    += 1

            count     -= abs(countSegment - currRule)
            ruleIndex += 1

    return count
