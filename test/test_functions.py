from unnamed.unnamed import run_test
from unnamed.evaluate import EvaluateException
from unnamed.parsetree import ParseException
from test.base_test_case import BaseTestCase

simple0 = """
            function a() {
              return 1;
            }
            function b() {
              return 2;
            }
            print a() + b();
          """
simple1 = """
            function addOne(a) {
              return a + 1;
            }
            function addTwo(a) {
              return 1 + addOne(a);
            }
            print addTwo(5);
          """
simple2 = """
            function lotsOfParams(a, b, c) {
              return b;
            }
            print lotsOfParams(1, 2, 3);
          """
simple3 = """
            function lotsOfParams(a, b, c, d) {
              print d;
              print a;
              return b;
            }
            print lotsOfParams(1, 2, 3, 4);
          """
simple4 = """
            let a = 8;
            function addOne(a) {
              return a + 1;
            }
            print a;
            a = addOne(a);
            print a;
          """
simple5 = """
            function max(a, b) {
              if (a > b) {
                return a;
              } else {
                return b;
              }
            }
            print max(1,2);
            print max(4,3);
            print max(6,6);
          """
simple6 = """
            function addOne(a) {
              return a + 1;
            }
            function addTwo(a) {
              return addOne(addOne(a));
            }
            print addOne(5);
            print addTwo(5);
          """
simple7 = """
            function printNumber(a) {
              print a;
              return 0;
            }
            let a = 0;
            loop(let i = 0; i < 10; i = i + 1;) {
              a = printNumber(i);
            }
          """
earlyreturn = """
                function addOne(a) {
                  if (True) {
                    return a + 1;
                  }
                  print 0;
                }
                print addOne(0);
              """
recursion0 = """
               function addOneUntilTen(a) {
                 if (a == 10) {
                   return a;
                 } else {
                   return addOneUntilTen(a + 1);
                 }
               }
               let n = 0;
               print n;
               n = addOneUntilTen(n);
               print n;
             """
recursion1 = """
               function addTwo(a) {
                 print a;
                 if (a == 10) {
                   return a;
                 } else {
                   return SubOne(a + 2);
                 }
               }
               function SubOne(a) {
                 print a;
                 if (a == 10) {
                   return a;
                 } else {
                   return addTwo(a - 1);
                 }
               }
               let n = 0;
               n = addTwo(n);
             """
fibonacci = """
              function fib(n) {
                let a = 0;
                let b = 1;
                let next = 0;
                loop(let i = 1; i < n; i = i + 1;) {
                  next = a + b;
                  a = b;
                  b = next;
                }
                return b;
              }
              print fib(14);
            """

class FunctionTest(BaseTestCase):
  def test_simple0(self):
    self.assert_stdout(simple0, '3\n')

  def test_simple1(self):
    self.assert_stdout(simple1, '7\n')

  def test_simple2(self):
    self.assert_stdout(simple2, '2\n')

  def test_simple3(self):
    self.assert_stdout(simple3, '4\n1\n2\n')

  def test_simple4(self):
    self.assert_stdout(simple4, '8\n9\n')

  def test_simple5(self):
    self.assert_stdout(simple5, '2\n4\n6\n')

  def test_simple6(self):
    self.assert_stdout(simple6, '6\n7\n')

  def test_simple7(self):
    self.assert_stdout(simple7, '0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n')

  def test_earlyreturn(self):
    self.assert_stdout(earlyreturn, '1\n')

  def test_recursion0(self):
    self.assert_stdout(recursion0, '0\n10\n')

  def test_recursion1(self):
    # Mutual recursion!
    self.assert_stdout(recursion1, "0\n2\n1\n3\n2\n4\n3\n5\n4\n6\n5\n7\n6\n8\n7\n9\n8\n10\n")

  def test_fibonacci(self):
    self.assert_stdout(fibonacci, '377\n')

if __name__ == '__main__':
  unittest.main()