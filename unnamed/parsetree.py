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

class MunchException(Exception):
  def __init__(self, message=None):
    if message is None:
      self.message = "Munch error!"
    self.message = message

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

  def build(self):
    self._munch([Tokens.BOF])

    retval = self._statements()
    if self._curr_token().token != Tokens.EOF:
      raise ParseException("Didn't finish parsing!")
    elif retval is None:
      raise ParseException("No result!")
    return retval

  ###########
  # Helpers #
  ###########

  def print_tokens(self):
    for token in self.program:
      token.print()

  def _prev_token(self):
    self.pos -= 1
    if (self.pos < 0):
      raise MunchException("Out of bounds!")
    return

  def _next_token(self):
    self.pos += 1
    if (self.pos == self.length):
      raise MunchException("Out of bounds!")
    return

  def _curr_token(self):
    return self.program[self.pos]

  def _munch(self, token_types):
    munched = self._curr_token()
    if munched.token in token_types:
      self._next_token()
      return munched
    raise MunchException("Munch error at " + self._curr_token().lexeme)

  def _munch_and_add_chain(self, types, retnode):
    for token_types in types:
      munched = self._munch(token_types)
      retnode.add_child(Node(munched.token, munched))
    return True
  
  def _munch_and_add(self, token_types, retnode):
    munched = self._munch(token_types)
    retnode.add_child(Node(munched.token, munched))
    return True

  def _peek(self, n):
    # Takes a peek at the next n tokens ahead without munching them
    # Hacky but it's too late to redesign my grammar :(
    tmp = self.pos
    tokens = []
    for i in range(0, n):
      if (tmp == self.length):
        raise MunchException("Out of bounds!")
      tokens.append(self.program[tmp].token)
      tmp += 1
    return tokens

  ##################
  # Building nodes #
  ##################

  def _statements(self):
    retnode = Node(Nonterminals.STATEMENTS)
    try:
      retnode.add_child(self._statement())
    except MunchException:
      return None

    retnode.add_child(self._statements())
    return retnode

  def _statement(self):
    retnode = Node(Nonterminals.STATEMENT)
    statement_tokens = []
    munched = False
    try:
      munched = self._munch_and_add([Tokens.RETURN], retnode)
      retnode.add_child(self._bexpr())
      munched = self._munch_and_add([Tokens.SEMICOLON], retnode)
      return retnode
    except MunchException:
      if munched:
        raise ParseException
      retnode = Node(Nonterminals.STATEMENT)

    try:
      munched = self._munch_and_add_chain(
        [
          [Tokens.FUNCTION],
          [Tokens.ID],
          [Tokens.LBRAC],
        ],
        retnode,
      )
      retnode.add_child(self._params())
      munched = self._munch_and_add_chain(
        [
          [Tokens.RBRAC],
          [Tokens.LCURLY],
        ],
        retnode,
      )
      retnode.add_child(self._statements())
      munched = self._munch_and_add([Tokens.RCURLY], retnode)
      return retnode
    except MunchException:
      if munched:
        raise ParseException
      retnode = Node(Nonterminals.STATEMENT)

    try:
      munched = self._munch_and_add_chain(
        [
          [Tokens.LOOP],
          [Tokens.LBRAC],
        ],
        retnode,
      )
      retnode.add_child(self._looprules())
      munched = self._munch_and_add_chain(
        [
          [Tokens.RBRAC],
          [Tokens.LCURLY],
        ],
        retnode,
      )
      retnode.add_child(self._statements())
      munched = self._munch_and_add([Tokens.RCURLY], retnode)
      return retnode
    except MunchException:
      if munched:
        raise ParseException
      retnode = Node(Nonterminals.STATEMENT)

    try:
      munched = self._munch_and_add_chain(
        [
          [Tokens.IF],
          [Tokens.LBRAC],
        ],
        retnode,
      )
      retnode.add_child(self._bexpr())
      munched = self._munch_and_add_chain(
        [
          [Tokens.RBRAC],
          [Tokens.LCURLY],
        ],
        retnode,
      )
      retnode.add_child(self._statements())
      munched = self._munch_and_add([Tokens.RCURLY], retnode)
      retnode.add_child(self._elif())
      return retnode
    except MunchException:
      if munched:
        raise ParseException
      retnode = Node(Nonterminals.STATEMENT)

    try:
      # Declaring a variable
      munched = self._munch_and_add_chain(
        [
          [Tokens.LET],
          [Tokens.ID],
          [Tokens.BECOMES],
        ],
        retnode
      )

      retnode.add_child(self._bexpr())
      munched = self._munch_and_add([Tokens.SEMICOLON], retnode)
      return retnode
    except MunchException:
      if munched:
        raise ParseException
      retnode = Node(Nonterminals.STATEMENT)

    try:
      # Need to peek since reassignments and 
      # function calls share a prefix in ID :(
      peeked = self._peek(2)
      if not (
        peeked[0] == Tokens.ID
        and peeked[1] == Tokens.BECOMES
      ):
        raise MunchException("Dummy exception!")

      munched = self._munch_and_add_chain(
        [
          [Tokens.ID],
          [Tokens.BECOMES],
        ],
        retnode
      )

      retnode.add_child(self._bexpr())
      munched = self._munch_and_add([Tokens.SEMICOLON], retnode)
      return retnode
    except MunchException:
      if munched:
        raise ParseException
      retnode = Node(Nonterminals.STATEMENT)

    try:
      # Printing a line
      munched = self._munch_and_add([Tokens.PRINT], retnode)
      retnode.add_child(self._bexpr())
      munched = self._munch_and_add([Tokens.SEMICOLON], retnode)
      return retnode
    except MunchException:
      if munched:
        raise ParseException
      retnode = Node(Nonterminals.STATEMENT)

    retnode.add_child(self._bexpr())
    self._munch_and_add([Tokens.SEMICOLON], retnode)
    return retnode

  def _pipe(self):
    retnode = Node(Nonterminals.PIPE)
    munched = False
    try:
      munched = self._munch_and_add([Tokens.INTO], retnode)
      retnode.add_child(self._callfunc())
    except MunchException:
      if munched:
        raise ParseException
      return retnode

  def _callfunc(self):
    retnode = Node(Nonterminals.CALLFUNC)
    munched = False
    try:
      munched = self._munch_and_add_chain(
        [
          [Tokens.ID],
          [Tokens.LBRAC],
        ],
        retnode,
      )
      retnode.add_child(self._args())
      munched = self._munch_and_add([Tokens.RBRAC], retnode)
      retnode.add_child(self._pipe())
      return retnode
    except MunchException:
      if munched:
        raise ParseException
      return retnode

  def _args(self):
    retnode = Node(Nonterminals.ARGS)
    munched = False
    try:
      # If we can't munch an expr, return empty Node
      retnode.add_child(self._bexpr())
      # If we munched a bexpr but not a comma, return the Node with the bexpr child
      self._munch_and_add([Tokens.COMMA], retnode)
    except MunchException:
      return retnode
    
    retnode.add_child(self._args())
    return retnode

  def _params(self):
    retnode = Node(Nonterminals.PARAMS)
    munched = False
    try:
      # If we can't munch an expr, return empty Node
      self._munch_and_add([Tokens.ID], retnode)
      # If we munched a bexpr but not a comma, return the Node with the bexpr child
      self._munch_and_add([Tokens.COMMA], retnode)
    except MunchException:
      return retnode
    
    retnode.add_child(self._params())
    return retnode

  def _looprules(self):
    retnode = Node(Nonterminals.LOOPRULES)
    try:
      retnode.add_child(self._bexpr())
      return retnode
    except MunchException:
      pass

    retnode.add_child(self._statement())
    retnode.add_child(self._bexpr())
    self._munch_and_add([Tokens.SEMICOLON], retnode)
    retnode.add_child(self._statement())

    return retnode

  def _elif(self):
    retnode = Node(Nonterminals.ELIFS)
    munched = False
    try:
      munched = self._munch_and_add_chain(
        [
          [Tokens.ELIF],
          [Tokens.LBRAC],
        ],
        retnode,
      )
      retnode.add_child(self._bexpr())
      munched = self._munch_and_add_chain(
        [
          [Tokens.RBRAC],
          [Tokens.LCURLY],
        ],
        retnode,
      )
      retnode.add_child(self._statements())
      munched = self._munch_and_add([Tokens.RCURLY], retnode)
      retnode.add_child(self._elif())
      return retnode
    except MunchException:
      if munched:
        raise ParseException
      retnode = Node(Nonterminals.ELIFS)

    try:
      munched = self._munch_and_add([Tokens.ELSE], retnode)
    except MunchException:
      if munched:
        raise ParseException
      return Node(Nonterminals.ELIFS)

    self._munch_and_add([Tokens.LCURLY], retnode)
    retnode.add_child(self._statements())
    self._munch_and_add([Tokens.RCURLY], retnode)
    return retnode

  def _bexpr(self):
    retnode = Node(Nonterminals.BEXPR)
    retnode.add_child(self._test())
    retnode.add_child(self._bexprF())
    return retnode

  def _bexprF(self):
    retnode = Node(Nonterminals.BEXPRF)
    munched = False
    try:
      munched = self._munch_and_add([Tokens.AND, Tokens.OR], retnode)
    except MunchException:
      if munched:
        raise ParseException
      return None

    retnode.add_child(self._test())
    retnode.add_child(self._bexprF())
    return retnode

  def _test(self):
    retnode = Node(Nonterminals.TEST)
    munched = False
    # Try to munch an OP
    try:
      # Could be not test
      munched = self._munch_and_add([Tokens.NOT], retnode)
      retnode.add_child(self._test())
      return retnode
    except MunchException:
      if munched:
        raise ParseException
      retnode = Node(Nonterminals.TEST)

    retnode.add_child(self._expr())
    try:
      munched = self._munch_and_add(
        [
          Tokens.GT,
          Tokens.LT,
          Tokens.NEQ,
          Tokens.EQ,
          Tokens.LEQ,
          Tokens.GEQ,
        ],
        retnode
      )
      retnode.add_child(self._expr())
      return retnode
    except MunchException:
      if munched:
        raise ParseException
      return retnode

  def _expr(self):
    retnode = Node(Nonterminals.EXPR)
    retnode.add_child(self._factor())
    retnode.add_child(self._exprF())
    return retnode

  def _exprF(self):
    retnode = Node(Nonterminals.EXPRF)
    munched = False
    try:
      munched = self._munch_and_add([Tokens.PLUS, Tokens.MINUS], retnode)
    except MunchException:
      if munched:
        raise ParseException 
      return None

    retnode.add_child(self._factor())
    retnode.add_child(self._exprF())
    return retnode

  def _factor(self):
    retnode = Node(Nonterminals.FACTOR)
    retnode.add_child(self._pow())
    retnode.add_child(self._factorF())
    return retnode

  def _factorF(self):
    retnode = Node(Nonterminals.FACTORF)
    munched = False
    try:
      munched = self._munch_and_add([Tokens.MULT, Tokens.DIV], retnode)
    except MunchException:
      if munched:
        raise ParseException
      return None

    retnode.add_child(self._pow())
    retnode.add_child(self._factorF())
    return retnode

  def _pow(self):
    retnode = Node(Nonterminals.POW)
    retnode.add_child(self._term())
    retnode.add_child(self._powF())
    return retnode

  def _powF(self):
    retnode = Node(Nonterminals.POWF)
    munched = False
    try:
      munched = self._munch_and_add([Tokens.EXP], retnode)
    except MunchException:
      if munched:
        raise ParseException
      return None

    retnode.add_child(self._term())
    retnode.add_child(self._powF())
    return retnode

  def _term(self):
    retnode = Node(Nonterminals.TERM)
    try:
      self._munch_and_add([Tokens.QUOTE], retnode)
      # Eat tokens until you eat a string
      while True:
        try:
          self._munch_and_add([Tokens.QUOTE], retnode)
          break
        except MunchException:
          self._munch_and_add([Tokens.STRING], retnode)

      return retnode
    except MunchException:
      pass

    try:
      self._munch_and_add([Tokens.TRUE, Tokens.FALSE], retnode)
      return retnode
    except MunchException:
      pass

    try:
      self._munch_and_add([Tokens.NUM], retnode)
      return retnode
    except MunchException:
      pass

    try:
      munched = False
      peeked = self._peek(2)
      if (
        peeked[0] == Tokens.ID
        and peeked[1] == Tokens.LBRAC
      ):
        retnode.add_child(self._callfunc())
        return retnode
      else:
        self._munch_and_add([Tokens.ID], retnode)
        return retnode
    except MunchException:
      if munched:
        raise ParseException
      
    try:
      self._munch_and_add([Tokens.MINUS], retnode)
      retnode.add_child(self._term())
      return retnode
    except MunchException:
      # Must be LBRAC expr RBRAC
      pass

    self._munch_and_add([Tokens.LBRAC], retnode)
    retnode.add_child(self._bexpr())
    self._munch_and_add([Tokens.RBRAC], retnode)
    return retnode
