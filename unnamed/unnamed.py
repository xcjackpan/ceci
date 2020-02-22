import sys, os, stat
from unnamed.tokenizer import *
from unnamed.cfg import *
from unnamed.evaluate import *

def preprocess(line):
  line = line.replace("(", " ( ")
  line = line.replace(")", " ) ")
  line = line.replace("-", " - ")
  line = line.replace(",", " , ")
  line = line.replace("\"", " \" ")
  return line

def main():
  mode = os.fstat(0).st_mode
  if stat.S_ISREG(mode) or stat.S_ISFIFO(mode):
    program = []
    for line in sys.stdin:
      line = preprocess(line)
      for word in line.split():
        program.append(word)

    tokenized = tokenize(program)
    #for token in tokenized:
    #  token.print()
    parsetree = ParseTree(tokenized)
    #parsetree.print_tokens()
    parsed = parsetree.build()
    #parsed.print()
    evaluator = Evaluator(parsed)
    evaluator.evaluate_tree()
  else:
    print("> ", end="", flush=True)
    evaluator = Evaluator(None)
    preprocessed = []
    for line in sys.stdin:
      if (line == "quit\n"):
        print("Bye!", flush=True)
        return
      line = preprocess(line)
      for word in line.split():
        preprocessed.append(word)
      tokenized = tokenize(preprocessed)
      parsetree = ParseTree(tokenized)
      try:
        parsed = parsetree.build()
      except ParseException:
        continue
      evaluator.update_tree(parsed)
      evaluator.evaluate_tree()
      print("> ", end="", flush=True)
      preprocessed = []

def run_test(input_program):
  # Driver for tests
  program = []
  input_program = preprocess(input_program)
  for word in input_program.split():
    program.append(word)

  tokenized = tokenize(program)
  parsetree = ParseTree(tokenized)
  parsed = parsetree.build()
  evaluator = Evaluator(parsed)
  evaluator.evaluate_tree()

if __name__ == "__main__":
  main()