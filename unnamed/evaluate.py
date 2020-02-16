from unnamed.tokenizer import *
from unnamed.cfg import *
from unnamed.parsetree import *

#TODO: Refactor out repetitive code ... but it's late rn

class EvaluateException(Exception):
  def __init__(self, message=None):
    if message is None:
      self.message = "Evaluation error!"
    self.message = message

class Evaluator:
  def __init__(self, parsetree):
    self.parsetree = parsetree
    # TODO: Refactor into table of tables
    self.symtable = {}

  def evaluate_tree(self):
    return self._evaluate(self.parsetree)

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

  def _evaluate(self, node):
    if node.type == Nonterminals.STATEMENTS:
      self._statements(node)
      return None
    elif node.type == Nonterminals.STATEMENT:
      return self._statement(node)
    elif node.type == Nonterminals.EXPR:
      return self._expr(node)
    elif node.type == Nonterminals.FACTOR:
      return self._factor(node)
    elif node.type == Nonterminals.POW:
      return self._eval_pow(node)
    elif node.type == Nonterminals.TERM:
      return self._term(node)
    elif node.type == Nonterminals.TEST:
      return self._test(node)
    elif node.type == Nonterminals.TESTF:
      return self._testF(node)
    elif node.type == Nonterminals.TESTB:
      return self._testB(node)

  def _statements(self, node):
    if len(node.children) == 2:
      self._statement(node.children[0])
      self._statements(node.children[1])
    elif len(node.children) == 1:
      self._statement(node.children[0])

  def _statement(self, node):
    length = len(node.children)
    if length == 4:
      # LET ID BECOMES EXPR
      is_decl = (
        node.children[0].type == Tokens.LET
        and node.children[1].type == Tokens.ID
        and node.children[2].type == Tokens.BECOMES
        and node.children[3].type == Nonterminals.EXPR
      )
      if is_decl:
        result = self._expr(node.children[3])
        self._add_to_symtable(node.children[1].token.lexeme, result)
    elif length == 3:
      is_assignment = (
        node.children[0].type == Tokens.ID
        and node.children[1].type == Tokens.BECOMES
        and node.children[2].type == Nonterminals.EXPR
      )
      if is_assignment:
        result = self._expr(node.children[2])
        self._update_in_symtable(node.children[0].token.lexeme, result)
    elif length == 2:
      is_print = (
        node.children[0].type == Tokens.PRINT
        and (
          node.children[1].type == Nonterminals.EXPR
          or node.children[1].type == Nonterminals.TEST
        )
      )
      if is_print:
        result = self._evaluate(node.children[1])
        print(str(result))
    elif length == 1:
      if node.children[0].type == Nonterminals.EXPR:
        return self._expr(node.children[0])
      elif node.children[0].type == Nonterminals.TEST:
        return self._test(node.children[0])

  def _test(self, node):
    left = self._evaluate(node.children[0])
    if len(node.children) == 1:
      return left
    return self._testF(left, node.children[1])

  def _testF(self, left, node):
    # Could be AND or OR
    if node.children[0].type == Tokens.AND:
      left = left and self._evaluate(node.children[1])
    else:
      left = left or self._evaluate(node.children[1])

    if len(node.children) == 3:
      return self._testF(left, node.children[2])
    return left

  def _testB(self, node):
    #stest -> EXPR GT EXPR
    #stest -> EXPR LT EXPR
    #stest -> EXPR NEQ EXPR
    #stest -> EXPR EQ EXPR
    #stest -> LPAREN test RPAREN
    #stest -> NOT stest
    #stest -> True
    #stest -> False
    length = len(node.children)
    if length == 3:
      if node.children[0].type == Tokens.LPAREN:
        return self._evaluate(node.children[1])
      
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
      return True if lexeme is "False" else "True"
    elif length == 1:
      lexeme = node.children[0].token.lexeme
      return True if lexeme is "True" else "False"

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
    if length == 1:
      # Either an ID or a num
      if node.children[0].type == Tokens.ID:
        return self._get_from_symtable(node.children[0].token.lexeme)
      elif node.children[0].type == Tokens.NUM:
        return int(node.children[0].token.lexeme)
    elif length == 2:
      # Unary minus
      return -1 * self._term(node.children[1])
    else:
      # Expression in brackets
      return self._expr(node.children[1])
