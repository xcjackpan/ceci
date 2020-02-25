from unnamed.unnamed import run_test
from unnamed.parsetree import ParseException
from test.base_test_case import BaseTestCase

simple0 = "print 1 + 1;"
simple1 = "print 1 + 3 - 4;"
associativity = "print 1 - 5 + 6;"
simple2 = "print 3 * 6;"
simple3 = "print 6 / 2;"
doubledigit = "print 11 * 10 + 16 - 4 + 19;"
precedence0 = "print 1 + 5 * 6 + 1;"
precedence1 = "print 1 - 12 / 6;"
precedence2 = "print 2 * 5 ^ 6;"
precedence3 = "print (1 + 3) * (2 - 4);"
precedence4 = "print 1 - (8 + 4) * 10;"
nested0 = "print ((1 + 3) * 4);"
nested1 = "print (((3))) * (4 ^ (1 + 1));"
unary0 = "print 1 + -4;"
unary1 = "print -1 - -6;"
unary2 = "print --1 - --4;"
except0 = "1 + (8"
except1 = "1 +"

class MathTest(BaseTestCase):
  def test_simple0(self):
    self.assert_stdout(simple0, '2\n')

  def test_simple1(self):
    self.assert_stdout(simple1, '0\n')

  def test_associativity(self):
    self.assert_stdout(associativity, '2\n')

  def test_simple2(self):
    self.assert_stdout(simple2, '18\n')

  def test_simple3(self):
    self.assert_stdout(simple3, '3.0\n')

  def test_doubledigit(self):
    self.assert_stdout(doubledigit, '141\n')

  def test_precedence0(self):
    self.assert_stdout(precedence0, '32\n')

  def test_precedence1(self):
    self.assert_stdout(precedence1, '-1.0\n')

  def test_precedence2(self):
    self.assert_stdout(precedence2, '31250\n')

  def test_precedence3(self):
    self.assert_stdout(precedence3, '-8\n')

  def test_precedence4(self):
    self.assert_stdout(precedence4, '-119\n')

  def test_nested0(self):
    self.assert_stdout(nested0, '16\n')

  def test_nested1(self):
    self.assert_stdout(nested1, '48\n')

  def test_unary0(self):
    self.assert_stdout(unary0, '-3\n')

  def test_unary1(self):
    self.assert_stdout(unary1, '5\n')

  def test_unary2(self):
    self.assert_stdout(unary2, '-3\n')

  def test_except0(self):
    self.assert_exception(except0, ParseException)

  def test_except1(self):
    self.assert_exception(except1, ParseException)

if __name__ == '__main__':
  unittest.main()