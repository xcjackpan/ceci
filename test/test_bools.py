from unnamed.unnamed import run_test
from unnamed.evaluate import EvaluateException
from test.base_test_case import BaseTestCase

simple0 = """
            print True
            print False
          """

class BooleanExpressionTest(BaseTestCase):
  def test_simple0(self):
    self.assert_stdout(simple0, 'True\nFalse\n')

if __name__ == '__main__':
  unittest.main()