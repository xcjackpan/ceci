import unittest

import sys
sys.path.append("..")
from unnamed import *

simple0 = "1 + 1"
simple1 = "1 + 3 - 4"
associativity = "1 - 5 + 6"
simple2 = "3 * 6"
simple3 = "6 / 2"
doubledigit = "11 * 10 + 16 - 4 + 19"
precedence0 = "1 + 5 * 6 + 1"
precedence1 = "1 - 12 / 6"
precedence2 = "2 * 5 ^ 6"
precedence3 = "(1 + 3) * (2 - 4)"
precedence4 = "1 - (8 + 4) * 10"
nested0 = "((1 + 3) * 4)"
nested1 = "(((3))) * (4 ^ (1 + 1))"
unary0 = "1 + -4"
unary1 = "-1 - -6"

class MathTest(unittest.TestCase):
  def test_simple0(self):
    self.assertEqual(run_test(simple0), 2)

  def test_simple1(self):
    self.assertEqual(run_test(simple1), 0)

  def test_associativity(self):
    self.assertEqual(run_test(associativity), 2)

  def test_simple2(self):
    self.assertEqual(run_test(simple2), 18)

  def test_simple3(self):
    self.assertEqual(run_test(simple3), 3)

  def test_doubledigit(self):
    self.assertEqual(run_test(doubledigit), 141)

  def test_precedence0(self):
    self.assertEqual(run_test(precedence0), 32)

  def test_precedence1(self):
    self.assertEqual(run_test(precedence1), -1)

  def test_precedence2(self):
    self.assertEqual(run_test(precedence2), 31250)

  def test_precedence3(self):
    self.assertEqual(run_test(precedence3), -8)

  def test_precedence4(self):
    self.assertEqual(run_test(precedence4), -119)

  def test_nested0(self):
    self.assertEqual(run_test(nested0), 16)

  def test_nested1(self):
    self.assertEqual(run_test(nested1), 48)

  def test_unary0(self):
    self.assertEqual(run_test(unary0), -3)

  def test_unary1(self):
    self.assertEqual(run_test(unary1), 5)

if __name__ == '__main__':
  unittest.main()