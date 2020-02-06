import sys
from tokenizer import *

def main():
  program = []
  for line in sys.stdin:
    for word in line.split():
      program.append(word)

  try:
    tokenize(program)
  except TokenException as e:
    print(e.message)

if __name__ == "__main__":
  main()