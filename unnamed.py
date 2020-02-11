import sys
from tokenizer import *
from parsetree import *
from evaluate import *

def preprocess(line):
  line = line.replace("(", " ( ")
  line = line.replace(")", " ) ")
  line = line.replace("-", " - ")
  return line

def main():
  program = []
  for line in sys.stdin:
    line = preprocess(line)
    for word in line.split():
      program.append(word)

  tokenized = tokenize(program)
  parsetree = ParseTree(tokenized)
  #parsetree.print_tokens()
  parsed = parsetree.build()
  #parsed.print()

  print(evaluate(parsed))

def run_test(input_program):
  # Driver for tests
  program = []
  input_program = preprocess(input_program)
  for word in input_program.split():
    program.append(word)

  tokenized = tokenize(program)
  parsetree = ParseTree(tokenized)
  parsed = parsetree.build()
  
  return evaluate(parsed)

if __name__ == "__main__":
  main()