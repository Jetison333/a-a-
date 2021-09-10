import tokenizer
from enum import Enum, auto

TokenType = tokenizer.TokenType

class ExprType(Enum):
    PARAM = auto()
    FUNC = auto()
    NUM = auto()

class Function():
    def __init__(self, name, params = None, cases = None):
        self.name = name
        self.params = params
        self.cases = cases

    def __repr__(self):
        string = '<Function Object, name = %r' % self.name

        if self.params:
            string += ', params = %r' % self.params

        if self.cases:
            string += ', cases = %r' % self.cases

        string += '>'

        return string

    def copy(self):
        return Function(self.name, self.params, [x.copy() for x in self.cases])

class Expr():
    def __init__(self, literal = None, typ = False, isCalled = False, calls = None):
        self.literal = literal
        self.type = typ
        self.isCalled = isCalled
        self.calls = calls

    def __eq__(self, other):
        return self.type == other.type and self.literal == other.literal

    def copy(self):
        if self.type == ExprType.NUM:
            return Expr(self.literal,self.type)

        if self.isCalled == False:
            
            if self.type == ExprType.PARAM:
                return Expr(self.literal, self.type)
            
            return Expr(self.literal.copy(), self.type)

        if self.calls == None:
            return Expr(self.literal.copy(), self.type, self.isCalled)

        if isinstance(self.literal, str):
            return Expr(self.literal, self.type, self.isCalled, [[y.copy() for y in x] for x in self.calls])

        return Expr(self.literal.copy(), self.type, self.isCalled, [[y.copy() for y in x] for x in self.calls])


    def __repr__(self):
        string = '<Expr object, type = %s, literal = %r' % (self.type, self.literal)

        if self.isCalled:
            string += ', isCalled'

        if self.calls:
            string += ', calls = %r' % self.calls

        string += '>'

        return string


MISSING = Expr(0, typ=ExprType.NUM)
    
class Case():
    def __init__(self, first = MISSING, second = MISSING, returnVal = MISSING):
        self.first = first
        self.second = second
        self.returnVal = returnVal

    def copy(self):
        return Case(self.first.copy(),self.second.copy(),self.returnVal.copy())

    def __repr__(self):
        return '<Case object, first = %r, second = %r, returnVal = %r>' % (self.first, self.second, self.returnVal)




class Parser():
    def __init__(self, program):
        tokenize = tokenizer.Tokenizer(program)
        tokens = tokenize.tokens
        self.tokens = tokens
        self.current = 0
        self.functions = []
        self.parse()

    def advance(self):
        self.current += 1
        return self.tokens[self.current-1]

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current-1]

    def check(self, tokenType):
        return self.peek().type == tokenType

    def match(self, tokenType):
        if self.check(tokenType):
            self.advance()
            return True
        return False

    def parseFunc(self):
        name = self.advance().literal
        params = self.parseParams()
        cases = self.parseCases()
        return Function(name, params, cases)

    def parseParams(self):
        if self.match(TokenType.LEFTSQUARE):

            params = []
            while not self.match(TokenType.RIGHTSQUARE):
                params.append(self.advance())

                self.match(TokenType.COMMA)

            if params == []:
                return None
            return params

        return None

    def parseCases(self):
        if self.match(TokenType.LEFTCURLY):

            cases = []

            while not self.match(TokenType.RIGHTCURLY):
                cases.append(self.parseCase())

                self.match(TokenType.COMMA)

            return cases

    def parseCase(self):
        first = self.parseExpr()

        if self.match(TokenType.EQUALS):  
        
            second = self.parseExpr()
            
            self.match(TokenType.THEN)

            returnVal = self.parseExpr()

            return Case(first, second, returnVal)

        return Case(returnVal = first)

    def parseCall(self):

        self.match(TokenType.LEFTPARENTH)
        
        params = []

        while not self.match(TokenType.RIGHTPARENTH):

            params.append(self.parseExpr())

            self.match(TokenType.COMMA)

        return params

    def parseCalls(self):
        calls = []

        while self.check(TokenType.LEFTPARENTH):
            calls.append(self.parseCall())

        return calls

    def parseExpr(self):

        if self.match(TokenType.NAME):

            name = self.previous().literal

            if self.check(TokenType.LEFTPARENTH):

                calls = self.parseCalls()

                return Expr(literal = name, typ = ExprType.PARAM, isCalled = True, calls = calls)

            if self.check(TokenType.LEFTCURLY) or self.check(TokenType.LEFTSQUARE):
                self.current -= 1
                function = self.parseFunc()

                if self.check(TokenType.LEFTPARENTH):
                    calls = self.parseCalls()
                    return Expr(function, ExprType.FUNC, True, calls = calls)

                return Expr(function, ExprType.FUNC)
 
            return Expr(literal = name, typ = ExprType.PARAM)

        if self.match(TokenType.NUM):
            return Expr(typ = ExprType.NUM, literal = self.previous().literal)

    def parse(self):
        while self.current < len(self.tokens):
            self.functions.append(self.parseFunc())
        

def namesExpr(expr):
    if expr.type == ExprType.PARAM:
        
        if expr.isCalled:
            for call in expr.calls:
                for exprCalled in call:
                    for z in namesExpr(exprCalled):
                        yield z

        yield expr

    elif expr.type == ExprType.FUNC:
        for x in namesFunc(expr.literal):
            yield x

        if expr.isCalled:
            for call in expr.calls:
                for exprCalled in call:
                    for z in namesExpr(exprCalled):
                        yield z
        

def namesFunc(function):
    for case in function.cases:
        for expr in namesExpr(case.first):
            yield expr

        for expr in namesExpr(case.second):
            yield expr

        for expr in namesExpr(case.returnVal):
            yield expr

def yieldCalls(callLst):
    for call in callLst:
        for exprCalled in call:
            yield exprCalled

def casesFunc(function):
    for case in function.cases:
        yield case.first
        yield case.second
        yield case.returnVal

def parse(program):
    parser = Parser(program)

    return parser.functions

#parser = Parser('test{test{1}()}')
#print(parser.functions)
        
