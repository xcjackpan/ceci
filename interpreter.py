class ParseException(Exception):
  def __init__(self, message):
      self.message = message

class Interpreter:
  def __init__(self, program):
    self.program = program
    self.pos = 0
    # symbol table
    # other pos

  def _next_token(self):
    self.pos += 1
    return self.program[self.pos]

  def _curr_token(self):
    return self.program[self.pos]

  def _munch(self, token_type):
    # maximally so
    if self._curr_token.token != token_type:
      return
    raise ParseException("Munch failed at" + self._curr_token())

  def print_tokens(self):
    for token in self.program:
      token.print()

  def expr(self):
    #expr -> expr PLUS factor
    #expr -> expr MINUS factor
    #expr -> factor
    pass
