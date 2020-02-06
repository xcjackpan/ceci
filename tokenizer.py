from tokens import *

class TokenException(Exception):
  def __init__(self, message):
      self.message = message

def tokenize(program):
  tokenized_program = []
  for token in program:
    if token in Tokens.LEXEMES:
      tokenized_program.append((token, Tokens.LEXEMES[token]))
    elif len(token) == 1:
      tokenized_program.append(
        (token, Tokens.DIGIT if token.isdigit() else Tokens.ID)
      ) #Either digit or ID
    elif not token[0].isdigit():
      tokenized_program.append((token, Tokens.ID))
    else:
      raise TokenException("Token Error: " + token + " is not a valid token.")