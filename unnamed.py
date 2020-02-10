import sys
from tokenizer import *
from parsetree import *

def main():
  program = []
  for line in sys.stdin:
    for word in line.split():
      program.append(word)

  try:
    tokenized = tokenize(program)
  except TokenException as e:
    print(e.message)

  parsetree = ParseTree(tokenized)
  parsetree.print_tokens()

  parsed = parsetree.build()
  parsed.print()

if __name__ == "__main__":
  main()