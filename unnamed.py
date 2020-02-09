import sys
from tokenizer import *
from interpreter import *

def main():
  program = []
  for line in sys.stdin:
    for word in line.split():
      program.append(word)

  try:
    tokenized = tokenize(program)
  except TokenException as e:
    print(e.message)

  interpreter = Interpreter(tokenized)
  interpreter.print_tokens()

if __name__ == "__main__":
  main()