import sys
from tokenizer import *
from parsetree import *
from evaluate import *

def main():
  program = []
  for line in sys.stdin:
    for word in line.split():
      program.append(word)

  tokenized = tokenize(program)

  parsetree = ParseTree(tokenized)
  #parsetree.print_tokens()

  parsed = parsetree.build()
  #parsed.print()

  print(evaluate(parsed))

if __name__ == "__main__":
  main()