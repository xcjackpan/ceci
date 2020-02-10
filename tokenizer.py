class Tokens:
  ID = 0
  COMMENT = 1
  DECLARE_VAR = 2
  BECOMES = 3
  IF_STATEMENT = 4
  LBRAC = 5
  RBRAC = 6
  LCURLY = 7
  RCURLY = 8
  LOOP = 9
  COMMA = 10
  DOT = 11
  BREAK_LOOP = 12
  RETURN = 13
  DECLARE_FUNC = 14
  CALL_FUNC = 15
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
  DIGIT = 29
  EQ = 30
  NEQ = 31
  GEQ = 32
  LEQ = 33
  FALSE = 34
  TRUE = 35
  BOF = 36
  EOF = 37

  LEXEMES = {
    "//": COMMENT,
    "let": DECLARE_VAR,
    "=": BECOMES,
    "if": IF_STATEMENT,
    "(": LBRAC,
    ")": RBRAC,
    "{": LCURLY,
    "}": RCURLY,
    "loop": LOOP,
    ",": COMMA,
    ".": DOT,
    "break": BREAK_LOOP,
    "return": RETURN,
    "function": DECLARE_FUNC,
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
    "!==": NEQ,
    ">=": GEQ,
    "<=": LEQ,
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
      self.token = Tokens.DIGIT if lexeme.isdigit() else Tokens.ID
    elif not lexeme[0].isdigit():
      self.token = Tokens.ID
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