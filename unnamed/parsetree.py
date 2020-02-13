from unnamed.tokenizer import *
from unnamed.cfg import *

class Node:
  def __init__(self, name, token=None):
    self.children = []
    self.type = name
    self.token = token

  def add_child(self, child):
    if child is not None:
      self.children.append(child)

  def print(self):
    if self.token is not None:
      print(self.type, self.token.lexeme, end=" ")
    else:
      print(self.type)
    for child in self.children:
      child.print()

class ParseException(Exception):
  def __init__(self, message=None):
    if message is None:
      self.message = "Parse error!"
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

  def _munch(self, token_types=None):
    munched = self._curr_token()
    if token_types is None:
      return munched
    elif munched.token in token_types:
      self._next_token()
      return munched
    raise ParseException("Parse error at " + self._curr_token().lexeme)

  def _expr(self):
    retnode = Node(Nonterminals.EXPR)
    retnode.add_child(self._factor())
    retnode.add_child(self._exprF())
    return retnode

  def _exprF(self):
    try:
      op = self._munch([Tokens.PLUS, Tokens.MINUS])
    except ParseException:
      return None

    retnode = Node(Nonterminals.EXPRF)
    retnode.add_child(Node(op.token, op))
    retnode.add_child(self._factor())
    retnode.add_child(self._exprF())
    return retnode

  def _factor(self):
    retnode = Node(Nonterminals.FACTOR)
    retnode.add_child(self._pow())
    retnode.add_child(self._factorF())
    return retnode

  def _factorF(self):
    try:
      op = self._munch([Tokens.MULT, Tokens.DIV])
    except ParseException:
      return None

    retnode = Node(Nonterminals.FACTORF)
    retnode.add_child(Node(op.token, op))
    retnode.add_child(self._pow())
    retnode.add_child(self._factorF())
    return retnode

  def _pow(self):
    retnode = Node(Nonterminals.POW)
    retnode.add_child(self._term())
    retnode.add_child(self._powF())
    return retnode

  def _powF(self):
    try:
      op = self._munch([Tokens.EXP])
    except ParseException:
      return None

    retnode = Node(Nonterminals.POWF)
    retnode.add_child(Node(op.token, op))
    retnode.add_child(self._term())
    retnode.add_child(self._powF())
    return retnode

  def _term(self):
    retnode = Node(Nonterminals.TERM)
    try:
      munched = self._munch([Tokens.ID, Tokens.NUM])
      retnode.add_child(Node(munched.token, munched))
      return retnode
    except ParseException:
      # Either bracket or unary sub
      pass
      
    try:
      munched = self._munch([Tokens.MINUS])
      retnode.add_child(Node(munched.token, munched))
      retnode.add_child(self._term())
      return retnode
    except ParseException:
      # Must be LBRAC expr RBRAC
      pass

    munched = self._munch([Tokens.LBRAC])
    retnode.add_child(Node(munched.token, munched))
    retnode.add_child(self._expr())
    rbrac = self._munch([Tokens.RBRAC])
    retnode.add_child(Node(rbrac.token, rbrac))
    return retnode
