from tokenizer import *
from cfg import *

#TODO: Refactor out repetitive code ... but it's late rn

def evaluate(node):
  if node.type == Nonterminals.EXPR:
    return expr(node)
  elif node.type == Nonterminals.FACTOR:
    return factor(node)
  elif node.type == Nonterminals.POW:
    return eval_pow(node)
  elif node.type == Nonterminals.TERM:
    return term(node)

def expr(node):
  left = evaluate(node.children[0])
  if len(node.children) == 1:
    return left
  return exprF(left, node.children[1])

def exprF(left, node):
  # Receives an EXPRF node
  # expr' -> PLUS factor expr'
  # expr' -> MINUS factor expr'

  if node.children[0].type == Tokens.PLUS:
    left = left + evaluate(node.children[1])
  else:
    left = left - evaluate(node.children[1])
  
  if len(node.children) == 3:
    return exprF(left, node.children[2])
  return left

def factor(node):
  left = evaluate(node.children[0])
  if len(node.children) == 1:
    return left
  return factorF(left, node.children[1])

def factorF(left, node):
  if node.children[0].type == Tokens.MULT:
    left = left * evaluate(node.children[1])
  else:
    left = left / evaluate(node.children[1])
  
  if len(node.children) == 3:
    return factorF(left, node.children[2])
  return left

def eval_pow(node):
  left = evaluate(node.children[0])
  if len(node.children) == 1:
    return left
  return eval_powF(left, node.children[1])

def eval_powF(left, node):
  left = left ** evaluate(node.children[1])
  
  if len(node.children) == 3:
    return eval_powF(left, node.children[2])
  return left

def term(node):
  length = len(node.children)
  if length == 1:
    # Either an ID or a num
    if node.children[0].type == Tokens.ID:
      # TODO: Variables
      pass
    elif node.children[0].type == Tokens.NUM:
      return int(node.children[0].token.lexeme)
  elif length == 2:
    # Unary minus
    return -1 * term(node.children[1])
  else:
    # Expression in brackets
    return expr(node.children[1])
