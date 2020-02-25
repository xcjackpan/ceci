from unnamed.unnamed import run_test
from unnamed.evaluate import EvaluateException
from test.base_test_case import BaseTestCase

simple0 = """
            print True;
            print False;
          """
simple1 = """
            print True and False;
            print False and True;
            print True or False;
            print False or True;
          """
simple2 = """
            print (False or True) and (False or True);
            print (True and False) or (True and False);
          """
simple3 = """
            print True and (False or True) and True;
          """
math0 = """
            print 1 + 2 < 3;
            print 1 + 2 < 3 + 2;
            print 1 + 2 == 3;
            print 1 + 2 == 3 + 2;
            print 1 + 2 > 3;
            print 1 + 2 > 3 + 2;
            print 1 + 2 >= 3;
            print 1 + 2 >= 3 + 2;
            print 1 + 2 <= 3;
            print 1 + 2 <= 3 + 2;
            print 1 + 2 != 3;
            print 1 + 2 != 3 + 2;
          """

class BooleanExpressionTest(BaseTestCase):
  def test_simple0(self):
    self.assert_stdout(simple0, 'True\nFalse\n')

  def test_simple1(self):
    self.assert_stdout(simple1, 'False\nFalse\nTrue\nTrue\n')

  def test_simple2(self):
    self.assert_stdout(simple2, 'True\nFalse\n')

  def test_simple3(self):
    self.assert_stdout(simple3, 'True\n')

  def test_math0(self):
    self.assert_stdout(
      math0,
      'False\nTrue\nTrue\nFalse\nFalse\nFalse\nTrue\nFalse\nTrue\nTrue\nFalse\nTrue\n'
    )

if __name__ == '__main__':
  unittest.main()