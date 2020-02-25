from unnamed.unnamed import run_test
from unnamed.evaluate import EvaluateException
from test.base_test_case import BaseTestCase

simple0 = """
            let a = 5;
            print a;
          """
simple1 = """
            let a = 5;
            let b = 3;
            print b;
            print a;
          """
simple2 = """
            let a = 5;
            let b = 3;
            print b + 1;
            print b - 1;
            print b;
            print b * 2;
            print b ^ 2;
          """
reassign0 = """
              let a = 0;
              print a;
              a = 1;
              print a;
              a = 0;
              print a;
            """
reassign1 = """
              let a = 1;
              print a;
              a = a + a + a;
              print a;
              a = a - a;
              print a;
            """
reassign2 = """
              let a = 1;
              let b = 2;
              print a;
              a = b;
              print a;
              a = a + b + 2;
              print a;
              print b;
            """
except0 = """
            print a;
          """
except1 = """
            a = 5;
          """
except2 = """
            let b = 0;
            b = a + 1;
          """

class VarsTest(BaseTestCase):
  def test_simple0(self):
    self.assert_stdout(simple0, '5\n')

  def test_simple1(self):
    self.assert_stdout(simple1, '3\n5\n')

  def test_simple2(self):
    self.assert_stdout(simple2, '4\n2\n3\n6\n9\n')

  def test_reassign0(self):
    self.assert_stdout(reassign0, '0\n1\n0\n')

  def test_reassign1(self):
    self.assert_stdout(reassign1, '1\n3\n0\n')

  def test_reassign2(self):
    self.assert_stdout(reassign2, '1\n2\n6\n2\n')

  def test_except0(self):
    self.assert_exception(except0, EvaluateException)

  def test_except1(self):
    self.assert_exception(except1, EvaluateException)

  def test_except2(self):
    self.assert_exception(except2, EvaluateException)

if __name__ == '__main__':
  unittest.main()