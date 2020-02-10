from tokenizer import *
from cfg import *

class Node:
  def __init__(self, name, token=None):
    self.children = []
    self.name = name
    self.token = token

  def add_child(self, child):
    self.children.append(child)

  def print(self):
    for child in self.children:
      child.print()
    if self.token is not None:
      print(self.name, self.token.lexeme)
    else:
      print(self.name)

class ParseException(Exception):
  def __init__(self, message):
      self.message = message

class ParseTree:
  def print_tokens(self):
    for token in self.program:
      token.print()

  def build(self):
    self._munch([Tokens.BOF])
    return self._expr()

  def __init__(self, program):
    self.program = program
    self.parsetree = None
    self.pos = 0
    self.length = len(program)
    # symbol table
    # other pos

  def _next_token(self):
    self.pos += 1
    if (self.pos > self.length):
      raise ParseException("Program over!")
    return

  def _curr_token(self):
    return self.program[self.pos]

  def _munch(self, token_types):
    munched = self._curr_token()
    if munched.token in token_types:
      self._next_token()
      return munched
    raise ParseException("Munch failed at" + self._curr_token().lexeme)

  def _expr(self):
    #expr -> factor PLUS expr
    #expr -> factor MINUS expr
    #expr -> factor

    #factor -> pow MULT factor
    #factor -> pow DIV factor
    #factor -> pow

    #pow -> term EXP pow
    #pow -> term

    #term -> ID
    #term -> DIGIT

    retnode = Node(Nonterminals.EXPR)
    left = self._factor()
    retnode.add_child(left)
    try:
      op = self._munch([Tokens.PLUS, Tokens.MINUS])
    except ParseException:
      return retnode
      
    retnode.add_child(Node(op.token, op))
    retnode.add_child(self._expr())
    return retnode

  def _factor(self):
    retnode = Node(Nonterminals.FACTOR)
    left = self._pow()
    retnode.add_child(left)
    try:
      op = self._munch([Tokens.MULT, Tokens.DIV])
    except ParseException:
      return retnode

    retnode.add_child(Node(op.token, op))
    retnode.add_child(self._factor())
    return retnode

  def _pow(self):
    retnode = Node(Nonterminals.POW)
    left = self._term()
    retnode.add_child(left)
    try:
      op = self._munch([Tokens.EXP])
    except ParseException:
      return retnode

    retnode.add_child(Node(op.token, op))
    retnode.add_child(self._pow())
    return retnode

  def _term(self):
    term = self._munch([Tokens.ID, Tokens.DIGIT])
    return Node(term.token, term)
  