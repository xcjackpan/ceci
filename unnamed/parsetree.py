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
  def __init__(self, program):
    self.program = program
    self.parsetree = None
    self.pos = 0
    self.length = len(program)

  def print_tokens(self):
    for token in self.program:
      token.print()

  def build(self):
    # TODO: Parsing TEST vs parsing EXPR
    # We can make TEST a node above EXPR ... make the boolean
    # ops be evaluated last, have type errors be EvaluateErrors
    self._munch([Tokens.BOF])

    retval = self._statements()
    if self._curr_token().token != Tokens.EOF:
      raise ParseException("Didn't finish parsing!")
    elif retval is None:
      raise ParseException("No result!")
    return retval

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
    raise ParseException("Parse error at " + self._curr_token().lexeme)

  def _statements(self):
    retnode = Node(Nonterminals.STATEMENTS)
    try:
      retnode.add_child(self._statement())
    except ParseException:
      return None

    retnode.add_child(self._statements())
    return retnode

  def _statement(self):
    retnode = Node(Nonterminals.STATEMENT)
    statement_tokens = []
    try:
      # Declaring a variable
      munched = self._munch([Tokens.LET])
      retnode.add_child(Node(munched.token, munched))
      munched = self._munch([Tokens.ID])
      retnode.add_child(Node(munched.token, munched))
      munched = self._munch([Tokens.BECOMES])
      retnode.add_child(Node(munched.token, munched))

      retnode.add_child(self._bexpr())
      return retnode
    except ParseException:
      retnode = Node(Nonterminals.STATEMENT)

    try:
      # Assigning a variable
      munched = self._munch([Tokens.ID])
      retnode.add_child(Node(munched.token, munched))
      munched = self._munch([Tokens.BECOMES])
      retnode.add_child(Node(munched.token, munched))

      retnode.add_child(self._bexpr())
      return retnode
    except ParseException:
      retnode = Node(Nonterminals.STATEMENT)

    try:
      # Printing a line
      munched = self._munch([Tokens.PRINT])
      retnode.add_child(Node(munched.token, munched))
      # TODO: What else could be printed??
      retnode.add_child(self._bexpr())
      return retnode
    except ParseException:
      retnode = Node(Nonterminals.STATEMENT)
  
    retnode.add_child(self._bexpr())
    return retnode
    #TODO: Other statement types

  def _bexpr(self):
    retnode = Node(Nonterminals.BEXPR)
    retnode.add_child(self._test())
    retnode.add_child(self._bexprF())
    return retnode

  def _bexprF(self):
    try:
      op = self._munch([Tokens.AND, Tokens.OR])
    except ParseException:
      return None
  
    retnode = Node(Nonterminals.BEXPRF)
    retnode.add_child(Node(op.token, op))
    retnode.add_child(self._test())
    retnode.add_child(self._bexprF())
    return retnode

  def _test(self):
    retnode = Node(Nonterminals.TEST)
    # Try to munch an OP
    try:
      # Could be not test
      munched = self._munch([Tokens.NOT])
      retnode.add_child(Node(munched.token, munched))
      retnode.add_child(self._test())
      return retnode
    except ParseException:
      retnode = Node(Nonterminals.TEST)

    retnode.add_child(self._expr())
    try:
      munched = self._munch([
        Tokens.GT,
        Tokens.LT,
        Tokens.NEQ,
        Tokens.EQ,
        Tokens.LEQ,
        Tokens.GEQ,
      ])
      retnode.add_child(Node(munched.token, munched))
      retnode.add_child(self._expr())
      return retnode
    except ParseException:
      return retnode

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
      munched = self._munch([Tokens.TRUE, Tokens.FALSE])
      retnode.add_child(Node(munched.token, munched))
      return retnode
    except ParseException:
      pass

    try:
      munched = self._munch([Tokens.ID, Tokens.NUM])
      retnode.add_child(Node(munched.token, munched))
      return retnode
    except ParseException:
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
    retnode.add_child(self._bexpr())
    rbrac = self._munch([Tokens.RBRAC])
    retnode.add_child(Node(rbrac.token, rbrac))
    return retnode
