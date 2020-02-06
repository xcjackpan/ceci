import sys
from tokenizer import *

def main():
  program = []
  for line in sys.stdin:
    for word in line.split():
      program.append(word)

  try:
    tokenized = tokenize(program)
  except TokenException as e:
    print(e.message)

  print(tokenized)

if __name__ == "__main__":
  main()