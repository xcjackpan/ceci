from unnamed.unnamed import run_test
from unnamed.evaluate import EvaluateException
from unnamed.parsetree import ParseException
from test.base_test_case import BaseTestCase

simple0 = """
            loop (let i = 0; i < 5; i = i + 1;) {
              print i;
            }
          """
simple1 = """
            let i = 0;
            loop (i < 5) {
              print i;
              i = i + 1;
            }
          """
simple2 = """
            print 0;
            loop (False) {
              print 0;
            }
          """

class LoopTest(BaseTestCase):
  def test_simple0(self):
    self.assert_stdout(simple0, '0\n1\n2\n3\n4\n')

  def test_simple1(self):
    self.assert_stdout(simple1, '0\n1\n2\n3\n4\n')

  def test_simple2(self):
    self.assert_stdout(simple2, '0\n')

if __name__ == '__main__':
  unittest.main()