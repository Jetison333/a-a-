from enum import Enum, auto
import re

nameStart = re.compile(r'[A-Za-z_]')
name = re.compile(r'\w')
numStart = re.compile(r'-|[0-9]')
num = re.compile(r'[0-9]')

class TokenType(Enum):
    NAME = 'name'
    NUM = 'number'
    LEFTPARENTH = '('
    RIGHTPARENTH = ')'
    LEFTSQUARE = '['
    RIGHTSQUARE = ']'
    LEFTCURLY = '{'
    RIGHTCURLY = '}'
    EQUALS = '='
    THEN = '>'
    COMMA = ','

class Token():
    def __init__(self, typ, lineNum, literal = None):
        self.type = typ
        self.lineNum = lineNum
        self.literal = literal

    def __repr__(self):
        rep = '<Token Object, type = %s' % self.type
        if type(self.literal) != None:
            rep += ' ,literal = %r ' % self.literal

        rep += ">"

        return rep

class Tokenizer():
    def __init__(self, program):
        self.program = program
        self.current = 0
        self.lineNumber = 1
        self.tokens = []
        self.parse()

    def advance(self):
        self.current += 1
        return self.program[self.current-1]

    def peek(self):
        if self.current == len(self.program):
            raise Exception("Unexpected EOF")
        return self.program[self.current]

    def addToken(self, token, literal = None):
        self.tokens.append(Token(token, self.lineNumber, literal))

    def parseName(self):
        
        string = ''

        string += self.advance()
        
        while name.match(self.peek()):
            string += self.advance()

        self.addToken(TokenType.NAME, string)

    def parseNum(self):

        numString = ''

        numString += self.advance()

        while num.match(self.peek()):
            numString += self.advance()

        self.addToken(TokenType.NUM, int(numString))

    def parse(self):

        while self.current < len(self.program):

            char = self.peek()
            
            if nameStart.match(char):
                self.parseName()

            elif numStart.match(char):
                self.parseNum()

            elif char == '(':
                self.addToken(TokenType.LEFTPARENTH)
                self.advance()

            elif char == ')':
                self.addToken(TokenType.RIGHTPARENTH)
                self.advance()

            elif char == '[':
                self.addToken(TokenType.LEFTSQUARE)
                self.advance()

            elif char == ']':
                self.addToken(TokenType.RIGHTSQUARE)
                self.advance()

            elif char == '{':
                self.addToken(TokenType.LEFTCURLY)
                self.advance()

            elif char == '}':
                self.addToken(TokenType.RIGHTCURLY)
                self.advance()

            elif char == '=':
                self.addToken(TokenType.EQUALS)
                self.advance()

            elif char == '>':
                self.addToken(TokenType.THEN)
                self.advance()

            elif char == ',':
                self.addToken(TokenType.COMMA)
                self.advance()

            elif char == '#':
                while char != '\n' and (self.current < len(self.program)):
                    char = self.advance()
                self.lineNumber += 1

            elif char == '\n':
                self.lineNumber += 1
                self.advance()

            else:
                self.advance()






























