class Tokens:
  ID = 0
  COMMENT = 1
  DECLARE_VAR = 2
  EQ = 3
  IF_STATEMENT = 4
  LBRAC = 5
  RBRAC = 6
  LCURLY = 7
  RCURLY = 8
  LOOP = 9
  COMMA = 10
  DOT = 11
  BREAK_LOOP = 12
  RETURN = 13
  DECLARE_FUNC = 14
  CALL_FUNC = 15
  PRINT = 16
  COLON = 17
  AND = 18
  OR = 19
  GT = 20
  LT = 21
  PLUS = 22
  MINUS = 23
  MULT = 24
  DIV = 25
  EXP = 26
  INTO = 27
  PIPE = 28
  DIGIT = 29

  LEXEMES = {
    "//": COMMENT,
    "let": DECLARE_VAR,
    "=": EQ,
    "if": IF_STATEMENT,
    "(": LBRAC,
    ")": RBRAC,
    "{": LCURLY,
    "}": RCURLY,
    "loop": LOOP,
    ",": COMMA,
    ".": DOT,
    "break": BREAK_LOOP,
    "return": RETURN,
    "function": DECLARE_FUNC,
    "print": PRINT,
    ":": COLON,
    "and": AND,
    "or": OR,
    ">": GT,
    "<": LT,
    "+": PLUS,
    "-": MINUS,
    "*": MULT,
    "/": DIV,
    "^": EXP,
    "into": INTO,
    "pipe": PIPE,
  }
