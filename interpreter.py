import sys
sys.setrecursionlimit(10**6)

import tokenizer
from AreturnsAparser import *


TokenType = tokenizer.TokenType
Token = tokenizer.Token

def numToExpr(num):
    return Expr(num, ExprType.NUM)

def strToFunc(string):
    i = Expr('i', ExprType.PARAM)
    caseList = []
    for index, char in enumerate(string):
        caseList.append(Case(i, numToExpr(index), numToExpr(ord(char))))

    caseList.append(Case(returnVal = numToExpr(0)))

    return Expr(Function('str', [Token(TokenType.NAME, -1, literal = 'i')], caseList), ExprType.FUNC)

def printFunc(func, funcMap):
    func.isCalled = True
    string = ''

    index = 0

    while True:
        
        func.calls = [[numToExpr(index)]]

        val = runFunc(func, funcMap).literal

        index += 1

        if val == 0:
            break

        print(chr(val),end='')

inputDict = {}
    
def runFunc(expr, funcMap):
    if str(expr) in inputDict:
        return inputDict[str(expr)].copy()
    result = run(expr.copy(), funcMap)
    inputDict[str(expr)] = result
    return result.copy()
    
def run(expr, funcMap):
    
    if expr.calls != []: #if the parameters in a call are called themselves, put the result of that call where that parameter was
        expr.calls[0] = [runFunc(x, funcMap) if x.isCalled else x for x in expr.calls[0]]
    
    if expr.type == ExprType.PARAM:   #checks if function is a name and not a function object, and if it is, replaces the literal with a copy of the function
        
        if expr.literal == 'inc':  #checks if function is intrinsic, and if it is do that instead
            numExpr = expr.calls[0][0]
            numExpr.literal += 1
            return numExpr

        if expr.literal == 'dec':
            numExpr = expr.calls[0][0]
            numExpr.literal -= 1
            return numExpr

        expr.type = ExprType.FUNC
        expr.literal = funcMap[expr.literal].copy()

    if expr.literal.params is None:
        if len(expr.calls[0]) > 0:
            raise Exception("'" + expr.literal.name + "' was called with the wrong number of parameters")
    elif len(expr.literal.params) != len(expr.calls[0]):
        raise Exception("'" + expr.literal.name + "' was called with the wrong number of parameters")

    
    varibles = {}
    if expr.literal.params != None:
        for index, param in enumerate(expr.literal.params):  #set up parameter hashmap
            varibles[param.literal] = expr.calls[0][index]

    for var in namesFunc(expr.literal): #change every instance of a parameter into the inputted parameter
        if var.literal in varibles:
            newVar = varibles[var.literal]
            var.literal = newVar.literal
            var.type = newVar.type

    for case in expr.literal.cases: #check all cases and return the first true one
        if case.first.isCalled:  #if cases are called, call them
            case.first = runFunc(case.first, funcMap)

        if case.second.isCalled:
            case.second = runFunc(case.second, funcMap)

        if case.first == case.second:
            
            if case.returnVal.isCalled:
                case.returnVal = runFunc(case.returnVal, funcMap)
                
            result = case.returnVal
            
            if len(expr.calls) > 1: #if the expr is called more than once, return the result of all the calls
                result.isCalled = True
                result.calls = expr.calls[1:]
                return runFunc(result, funcMap)
       
            else:
                return result

    raise Exception(expr.name + " did not return any value")



def runProgram(program):
    
    funclist = parse(program)

    try:
        main = next(filter(lambda x: x.name == 'main', funclist))
    except:
        raise("main not found")
    
    funcMap = {}
    for func in funclist:
        funcMap[func.name] = func
        
    if main.params != None:
        strFunc = strToFunc(input("input: "))
        calls = [[strFunc]]
    else:
        calls = [[]]
        
    result = runFunc(Expr(main, ExprType.FUNC, True, calls), funcMap)


    if result.type == ExprType.NUM:
        print(result.literal)

    else:
        printFunc(result, funcMap)

with open(sys.argv[1]) as f:
    program = f.read()


try:
    runProgram(program)
except Exception as msg:
    print(msg)





