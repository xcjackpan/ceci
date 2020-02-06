class BaseNode:
  def __init__(self):
    self.name = None
    self.root = None
    self.children = []

class Expression(BaseNode):
  # EXPR -> ID
  # EXPR -> DIGIT

  # EXPR -> ID PLUS EXPR
  # EXPR -> DIGIT PLUS EXPR
  # EXPR -> ID MINUS EXPR
  # EXPR -> DIGIT MINUS EXPR

  # FACTOR -> ID MULT EXPR
  # FACTOR -> DIGIT MULT EXPR
  # FACTOR -> ID DIV EXPR
  # FACTOR -> DIGIT DIV EXPR
  # FACTOR -> EXPR
  pass

class Statement(BaseNode):
  pass

class 