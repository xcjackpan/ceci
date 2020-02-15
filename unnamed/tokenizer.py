class Tokens:
  ID = 0
  COMMENT = 1
  LET = 2
  BECOMES = 3
  IF = 4
  LBRAC = 5
  RBRAC = 6
  LCURLY = 7
  RCURLY = 8
  LOOP = 9
  COMMA = 10
  DOT = 11
  BREAK = 12
  RETURN = 13
  FUNCTION = 14
  CALL_FUNC = 15 #Being used?
  PRINT = 16
  COLON = 17
  AND = 18
  OR = 19
  GT = 20
  LT = 21
  PLUS = 22
  MINUS = 23
  MULT = 24
  DIV = 25
  EXP = 26
  INTO = 27
  PIPE = 28
  NUM = 29
  EQ = 30
  NEQ = 31
  GEQ = 32
  LEQ = 33
  FALSE = 34
  TRUE = 35
  BOF = 36
  EOF = 37
  NOT = 38

  LEXEMES = {
    "//": COMMENT,
    "let": LET,
    "=": BECOMES,
    "if": IF,
    "(": LBRAC,
    ")": RBRAC,
    "{": LCURLY,
    "}": RCURLY,
    "loop": LOOP,
    ",": COMMA,
    ".": DOT,
    "break": BREAK,
    "return": RETURN,
    "function": FUNCTION,
    "print": PRINT,
    ":": COLON,
    "&&": AND,
    "||": OR,
    ">": GT,
    "<": LT,
    "+": PLUS,
    "-": MINUS,
    "*": MULT,
    "/": DIV,
    "^": EXP,
    "into": INTO,
    "pipe": PIPE,
    "==": EQ,
    "!=": NEQ,
    ">=": GEQ,
    "<=": LEQ,
    "not": NOT,
    "False": FALSE,
    "True": TRUE,
    "BOF": BOF,
    "EOF": EOF,
  }

class Token:
  def __init__(self, lexeme):
    self.lexeme = lexeme
    if lexeme in Tokens.LEXEMES:
      self.token = Tokens.LEXEMES[lexeme]
    elif len(lexeme) == 1:
      #Either digit or ID
      self.token = Tokens.NUM if lexeme.isdigit() else Tokens.ID
    elif lexeme[0].isalpha():
      self.token = Tokens.ID
    elif lexeme.isdigit():
      self.token = Tokens.NUM
    else:
      raise TokenException("Token Error: " + lexeme + " is not a valid token.")

  def print(self):
    print("(" + self.lexeme + ", "+ str(self.token) + ")")

class TokenException(Exception):
  def __init__(self, message):
      self.message = message

def tokenize(program):
  tokenized_program = [Token("BOF")]
  for token in program:
    tokenized_program.append(Token(token))
  tokenized_program.append(Token("EOF"))
  return tokenized_program