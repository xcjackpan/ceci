from unnamed.tokenizer import *
from unnamed.cfg import *
from unnamed.parsetree import *

#TODO: Refactor out repetitive code ... but it's late rn

class EvaluateException(Exception):
  def __init__(self, message=None):
    if message is None:
      self.message = "Evaluation error!"
    self.message = message

class ReturnValue(Exception):
  # Pretty hacky tbh but I don't have a good way to stop evaluating the
  # tree with my current code structure
  def __init__(self, value=None):
    self.value = value

class Evaluator:
  def __init__(self, parsetree):
    self.parsetree = parsetree
    self.symtable = {}
    self.functable = {}

  def update_tree(self, parsetree):
    self.parsetree = parsetree

  def evaluate_tree(self):
    try:
      return self._evaluate(self.parsetree)
    except ReturnValue as r:
      return r.value

  ##########################
  # Symtable and functable #
  ##########################

  def _add_to_functable(self, name, node):
    if name in self.functable:
      raise EvaluateException(name + " is already declared!")
    self.functable[name] = node

  def _get_from_functable(self, name):
    if name not in self.functable:
      raise EvaluateException(name + " is not defined!")
    return self.functable[name]

  def _add_to_symtable(self, name, value=None):
    if name in self.symtable:
      raise EvaluateException(name + " is already declared!")
    self.symtable[name] = value

  def _get_from_symtable(self, name):
    if name not in self.symtable:
      raise EvaluateException(name + " is not defined!")
    return self.symtable[name]

  def _update_in_symtable(self, name, value):
    if name not in self.symtable:
      raise EvaluateException(name + " is not defined!")
    self.symtable[name] = value  

  ####################
  # Evaluating nodes #
  ####################

  def _evaluate(self, node):
    if node.type == Nonterminals.STATEMENTS:
      return self._statements(node)
    elif node.type == Nonterminals.STATEMENT:
      return self._statement(node)
    elif node.type == Nonterminals.ELIFS:
      return self._elifs(node)
    elif node.type == Nonterminals.ARGS:
      return self._args(node)
    elif node.type == Nonterminals.PARAMS:
      return self._params(node)
    elif node.type == Nonterminals.BEXPR:
      return self._bexpr(node)
    elif node.type == Nonterminals.BEXPRF:
      return self._bexprF(node)
    elif node.type == Nonterminals.TEST:
      return self._test(node)
    elif node.type == Nonterminals.EXPR:
      return self._expr(node)
    elif node.type == Nonterminals.FACTOR:
      return self._factor(node)
    elif node.type == Nonterminals.POW:
      return self._eval_pow(node)
    elif node.type == Nonterminals.TERM:
      return self._term(node)

  def _statements(self, node):
    # RETURN needs to be done here since it must stop execution of the program
    length = len(node.children)
    if length > 0:
      if self._is_return(node.children[0]):
        raise ReturnValue(self._evaluate(node.children[0].children[1]))
      elif length == 2:
        self._statement(node.children[0])
        return self._statements(node.children[1])
      elif length == 1:
        self._statement(node.children[0])

  def _statement(self, node):
    length = len(node.children)
    if length == 8:
      is_if = (
        node.children[0].type == Tokens.IF
        and node.children[1].type == Tokens.LBRAC
        and node.children[2].type == Nonterminals.BEXPR
        and node.children[3].type == Tokens.RBRAC
        and node.children[4].type == Tokens.LCURLY
        and node.children[5].type == Nonterminals.STATEMENTS
        and node.children[6].type == Tokens.RCURLY
        and node.children[7].type == Nonterminals.ELIFS
      )
      if is_if:
        result = self._evaluate(node.children[2])
        if result:
          self._evaluate(node.children[5])
        elif not result:
          self._evaluate(node.children[7])
        else:
          raise EvaluateException("If-condition didn't return BOOL")

      is_function = (
        node.children[0].type == Tokens.FUNCTION
        and node.children[1].type == Tokens.ID
        and node.children[2].type == Tokens.LBRAC
        and node.children[3].type == Nonterminals.PARAMS
        and node.children[4].type == Tokens.RBRAC
        and node.children[5].type == Tokens.LCURLY
        and node.children[6].type == Nonterminals.STATEMENTS
        and node.children[7].type == Tokens.RCURLY
      )
      if is_function:
        self._add_to_functable(node.children[1].token.lexeme, node)
    elif length == 7:
      is_loop = (
        node.children[0].type == Tokens.LOOP
        and node.children[1].type == Tokens.LBRAC
        and node.children[2].type == Nonterminals.LOOPRULES
        and node.children[3].type == Tokens.RBRAC
        and node.children[4].type == Tokens.LCURLY
        and node.children[5].type == Nonterminals.STATEMENTS
        and node.children[6].type == Tokens.RCURLY
      )
      if is_loop:
        looprules = node.children[2]
        looprules_length = len(looprules.children)
        if looprules_length == 1:
          #TODO: Verify types?
          condition = self._evaluate(looprules.children[0])
          while (condition):
            self._evaluate(node.children[5])
            condition = self._evaluate(looprules.children[0])
        elif looprules_length == 4:
          # STATEMENT/BEXPR BEXPR SEMICOLON STATEMENT
          self._evaluate(looprules.children[0])
          condition = self._evaluate(looprules.children[1])
          while (condition):
            self._evaluate(node.children[5])
            self._evaluate(looprules.children[3])
            condition = self._evaluate(looprules.children[1])
    elif length == 5:
      is_decl = (
        node.children[0].type == Tokens.LET
        and node.children[1].type == Tokens.ID
        and node.children[2].type == Tokens.BECOMES
        and node.children[3].type == Nonterminals.BEXPR
        and node.children[4].type == Tokens.SEMICOLON
      )
      if is_decl:
        result = self._evaluate(node.children[3])
        self._add_to_symtable(node.children[1].token.lexeme, result)
    elif length == 4:
      is_assignment = (
        node.children[0].type == Tokens.ID
        and node.children[1].type == Tokens.BECOMES
        and node.children[2].type == Nonterminals.BEXPR
        and node.children[3].type == Tokens.SEMICOLON
      )
      if is_assignment:
        result = self._evaluate(node.children[2])
        self._update_in_symtable(node.children[0].token.lexeme, result)
    elif length == 3:
      is_print = (
        node.children[0].type == Tokens.PRINT
        and node.children[1].type == Nonterminals.BEXPR
        and node.children[2].type == Tokens.SEMICOLON
      )
      if is_print:
        result = self._evaluate(node.children[1])
        print(str(result))
    elif length == 2:
      if node.children[1].type == Tokens.SEMICOLON:
        return self._evaluate(node.children[0])

  def _pipe(self, node, pipe_input):
    return self._callfunc(node.children[1], pipe_input)

  def _callfunc(self, node, pipe_input=None):
    function_name = node.children[0].token.lexeme
    function_node = self._get_from_functable(function_name)
    function_evaluator = FunctionEvaluator(
      function_node,
      self._evaluate(node.children[2]),
      self.functable
    )
    if pipe_input is not None:
      function_evaluator._add_pipe_input(pipe_input)
    retval = function_evaluator.evaluate_tree()
    if len(node.children[4].children) > 0:
      return self._pipe(node.children[4], retval)
    else:
      return retval

  def _args(self, node):
    # Returns an array of argument values in order
    length = len(node.children)
    if length == 0:
      return []
    elif length == 1:
      return [self._evaluate(node.children[0])]
    elif length == 3:
      other_args = self._evaluate(node.children[2])
      other_args.insert(0, self._evaluate(node.children[0]))
      return other_args

  def _params(self, node):
    # Returns an array of param names in order
    # TODO: Update with PIPE
    length = len(node.children)
    if length == 0:
      return []
    elif length == 1:
      return [node.children[0].token.lexeme]
    elif length == 3:
      other_params = self._evaluate(node.children[2])
      other_params.insert(0, node.children[0].token.lexeme)
      return other_params

  def _elifs(self, node):
    length = len(node.children)
    if length != 0:
      if node.children[0].type == Tokens.ELIF:
        # elif LBRAC bexpr RBRAC LCURLY statements RCURLY ELIFS
        result = self._evaluate(node.children[2])
        if result:
          self._evaluate(node.children[5])
        elif not result:
          self._evaluate(node.children[7])
        else:
          raise EvaluateException("If-condition didn't return BOOL")
      elif node.children[0].type == Tokens.ELSE:
        # ELSE LCURLY statements RCURLY
        self._evaluate(node.children[2])

  def _bexpr(self, node):
    left = self._evaluate(node.children[0])
    if len(node.children) == 1:
      return left
    return self._bexprF(left, node.children[1])

  def _bexprF(self, left, node):
    if node.children[0].type == Tokens.AND:
      left = left and self._evaluate(node.children[1])
    else:
      left = left or self._evaluate(node.children[1])

    if len(node.children) == 3:
      return self._bexprF(left, node.children[2])
    return left

  def _test(self, node):
    #test -> EXPR GT EXPR
    #test -> EXPR LT EXPR
    #test -> EXPR NEQ EXPR
    #test -> EXPR EQ EXPR
    #test -> NOT test
    #test -> True
    #test -> False
    length = len(node.children)
    if length == 3:
      op = node.children[1].type
      left = self._evaluate(node.children[0])
      right = self._evaluate(node.children[2])
      if op == Tokens.GT:
        return left > right
      elif op == Tokens.LT:
        return left < right
      elif op == Tokens.NEQ:
        return left != right
      elif op == Tokens.EQ:
        return left == right
      elif op == Tokens.LEQ:
        return left <= right
      elif op == Tokens.GEQ:
        return left >= right
    elif length == 2:
      lexeme = self._evaluate(node.children[1])
      # TODO: Type error checking!
      return True if lexeme is "False" else "True"
    elif length == 1:
      # Must be just an expr
      return self._evaluate(node.children[0])

  def _expr(self, node):
    left = self._evaluate(node.children[0])
    if len(node.children) == 1:
      return left
    return self._exprF(left, node.children[1])

  def _exprF(self, left, node):
    # Receives an EXPRF node
    # expr' -> PLUS factor expr'
    # expr' -> MINUS factor expr'
    #TODO: Replace with direct exprF call
    if node.children[0].type == Tokens.PLUS:
      left = left + self._evaluate(node.children[1])
    else:
      left = left - self._evaluate(node.children[1])
    
    if len(node.children) == 3:
      return self._exprF(left, node.children[2])
    return left

  def _factor(self, node):
    left = self._evaluate(node.children[0])
    if len(node.children) == 1:
      return left
    return self._factorF(left, node.children[1])

  def _factorF(self, left, node):
    if node.children[0].type == Tokens.MULT:
      left = left * self._evaluate(node.children[1])
    else:
      left = left / self._evaluate(node.children[1])
    
    if len(node.children) == 3:
      return self._factorF(left, node.children[2])
    return left

  def _eval_pow(self, node):
    left = self._evaluate(node.children[0])
    if len(node.children) == 1:
      return left
    return self.eval_powF(left, node.children[1])

  def eval_powF(self, left, node):
    left = left ** self._evaluate(node.children[1])
    
    if len(node.children) == 3:
      return self.eval_powF(left, node.children[2])
    return left

  def _term(self, node):
    length = len(node.children)
    if length >= 1:
      if node.children[0].type == Tokens.QUOTE:
        ret = ""
        for node in node.children[1:-1]:
          ret = ret + " " + node.token.lexeme
        return ret[1:]
      elif length == 1:
        # Either an ID or a num
        if node.children[0].type == Tokens.ID:
          return self._get_from_symtable(node.children[0].token.lexeme)
        elif node.children[0].type == Tokens.NUM:
          return int(node.children[0].token.lexeme)
        elif node.children[0].type == Tokens.TRUE:
          return True
        elif node.children[0].type == Tokens.FALSE:
          return False
        elif node.children[0].type == Nonterminals.CALLFUNC:
          return self._callfunc(node.children[0])
      elif length == 2:
        # Unary minus
        return -1 * self._term(node.children[1])
      elif length == 3:
        if (
          node.children[0].type == Tokens.LBRAC
          and node.children[2].type == Tokens.RBRAC
        ):
          # Expression in brackets
          return self._bexpr(node.children[1])

  ###########
  # Helpers #
  ###########

  def _is_return(self, node):
    return (
      node.children[0].type == Tokens.RETURN
      and node.children[1].type == Nonterminals.BEXPR
      and node.children[2].type == Tokens.SEMICOLON
    )

class FunctionEvaluator(Evaluator):
  # Used to run functions
  def __init__(self, parsetree, args, functable):
    self.parsetree = parsetree
    self.functable = functable
    self.symtable = self._build_initial_symtable(args)

  def evaluate_tree(self):
    function_body_node = self.parsetree.children[6]
    if function_body_node.type != Nonterminals.STATEMENTS:
      raise EvaluateException("Didn't get function body!")

    try:
      return self._evaluate(function_body_node)
    except ReturnValue as r:
      return r.value

  def _build_initial_symtable(self, args):
    params_node = self.parsetree.children[3]
    if params_node.type != Nonterminals.PARAMS:
      raise EvaluateException("Didn't get params!")
    params = self._evaluate(params_node)
    return dict(zip(params, args))

  def _add_pipe_input(self, pipe_input):
    self.symtable["pipe"] = pipe_input