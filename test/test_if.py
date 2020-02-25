from unnamed.unnamed import run_test
from unnamed.evaluate import EvaluateException
from unnamed.parsetree import ParseException
from test.base_test_case import BaseTestCase

simple0 = """
            let a = 1;
            let b = 2;
            if (a > b) {
              print 0;
            } elif (b > a) {
              print 1;
            }
          """
simple1 = """
            let a = 1;
            let b = 2;
            if (a > b) {
              print 0;
            } else {
              print 1;
            }
          """
simple2 = """
            let a = 1;
            let b = 2;
            if (a < b) {
              print 0;
            } else {
              print 1;
            }
          """
simple3 = """
            let a = 1;
            let b = 2;
            if (a < b) {
              print 0;
            }
            print 1;
          """
simple4 = """
            let a = 1;
            let b = 2;
            if (a > b) {
              print 0;
            }
            print 1;
          """
simple5 = """
            if (True) {
              print 0;
              if (True) {
                print 1;
              } elif (True) {
                print 2;
              }
            }
          """
simple6 = """
            if (True) {
              print 0;
              if (False) {
                print 1;
              } elif (False) {
                print 2;
              } else {
                if (False) {
                  print 1;
                }
              }
            }
          """
simple7 = """
            if (True) { }
            if (False) { }
            print 0;
          """
except0 = """
            elif (False) {
              print 1;
            }
          """
except1 = """
            else (False) {
              print 1;
            }
          """
except2 = """
            if (True) {
              print 1;
          """
edge0 = """
          if (10 + 1) {
            print 0;
          } else {
            print 1;
          }
        """
edge1 = """
          if (1 - 1) {
            print 0;
          } else {
            print 1;
          }
        """

class IfTest(BaseTestCase):
  def test_simple0(self):
    self.assert_stdout(simple0, '1\n')

  def test_simple1(self):
    self.assert_stdout(simple1, '1\n')

  def test_simple2(self):
    self.assert_stdout(simple2, '0\n')

  def test_simple3(self):
    self.assert_stdout(simple3, '0\n1\n')

  def test_simple4(self):
    self.assert_stdout(simple4, '1\n')

  def test_simple5(self):
    self.assert_stdout(simple5, '0\n1\n')

  def test_simple6(self):
    self.assert_stdout(simple6, '0\n')

  def test_simple7(self):
    self.assert_stdout(simple7, '0\n')

  def test_except0(self):
    self.assert_exception(except0, ParseException)

  def test_except1(self):
    self.assert_exception(except1, ParseException)

  def test_except2(self):
    self.assert_exception(except2, ParseException)

  def test_edge0(self):
    self.assert_stdout(edge0, '0\n')

  def test_edge1(self):
    self.assert_stdout(edge1, '1\n')

if __name__ == '__main__':
  unittest.main()