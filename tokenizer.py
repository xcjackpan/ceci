from tokens import *

class TokenException(Exception):
  def __init__(self, message):
      self.message = message

def tokenize(program):
  tokenized = []
  for token in program:
    if token in Tokens.LEXEMES:
      print(token, Tokens.LEXEMES[token])
    elif len(token) > 1 and not token[0].isdigit():
      print(token, Tokens.ID)
    elif len(token) == 1:
      print(token, Tokens.DIGIT if token.isdigit() else Tokens.ID) #Either digit or ID
    else:
      raise TokenException("Token Error: " + token + " is not a valid token.")