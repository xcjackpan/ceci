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
  elif node.type == Tokens.ID:
    return term(node)
  elif node.type == Tokens.NUM:
    return int(node.token.lexeme)

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
