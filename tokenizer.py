from enum import Enum, auto
import re

nameStart = re.compile(r'[A-Za-z_]')
name = re.compile(r'\w')
numStart = re.compile(r'-|[0-9]')
num = re.compile(r'[0-9]')

class TokenType(Enum):
    NAME = auto()
    NUM = auto()
    LEFTPARENTH = auto()
    RIGHTPARENTH = auto()
    LEFTSQUARE = auto()
    RIGHTSQUARE = auto()
    LEFTCURLY = auto()
    RIGHTCURLY = auto()
    EQUALS = auto()
    THEN = auto()
    COMMA = auto()

class Token():
    def __init__(self, typ, literal = None):
        self.type = typ
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
        self.tokens = []
        self.parse()

    def advance(self):
        self.current += 1
        return self.program[self.current-1]

    def peek(self):
        return self.program[self.current]

    def parseName(self):
        
        string = ''

        string += self.advance()
        
        while name.match(self.peek()):
            string += self.advance()

        self.tokens.append(Token(TokenType.NAME, string))

    def parseNum(self):

        numString = ''

        numString += self.advance()

        while num.match(self.peek()):
            numString += self.advance()

        self.tokens.append(Token(TokenType.NUM, int(numString)))

    def parse(self):

        while self.current < len(self.program):

            char = self.peek()
            
            if nameStart.match(char):
                self.parseName()

            elif numStart.match(char):
                self.parseNum()

            elif char == '(':
                self.tokens.append(Token(TokenType.LEFTPARENTH))
                self.advance()

            elif char == ')':
                self.tokens.append(Token(TokenType.RIGHTPARENTH))
                self.advance()

            elif char == '[':
                self.tokens.append(Token(TokenType.LEFTSQUARE))
                self.advance()

            elif char == ']':
                self.tokens.append(Token(TokenType.RIGHTSQUARE))
                self.advance()

            elif char == '{':
                self.tokens.append(Token(TokenType.LEFTCURLY))
                self.advance()

            elif char == '}':
                self.tokens.append(Token(TokenType.RIGHTCURLY))
                self.advance()

            elif char == '=':
                self.tokens.append(Token(TokenType.EQUALS))
                self.advance()

            elif char == '>':
                self.tokens.append(Token(TokenType.THEN))
                self.advance()

            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA))
                self.advance()

            elif char == '#':
                while char != '\n' and (self.current < len(self.program)):
                    char = self.advance()

            else:
                self.advance()






























