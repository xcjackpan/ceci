from tokenizer import *
from cfg import *

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
  
  if node.children[1].type == Tokens.PLUS:
    return left + evaluate(node.children[2])
  else:
    return left - evaluate(node.children[2])

def factor(node):
  left = evaluate(node.children[0])
  if len(node.children) == 1:
    return left

  if node.children[1].type == Tokens.MULT:
    return left * evaluate(node.children[2])
  else:
    return left * evaluate(node.children[2])

def eval_pow(node):
  left = evaluate(node.children[0])
  if len(node.children) == 1:
    return left
  
  return left ** evaluate(node.children[2])
