from unnamed.unnamed import run_test
from unnamed.evaluate import EvaluateException
from unnamed.parsetree import ParseException
from test.base_test_case import BaseTestCase

simple0 = """
            function constantOne() {
              return 1;
            }
            function printPipe() {
              print pipe;
            }
            constantOne() into printPipe();
          """
simple1 = """
            function printPipe() {
              print pipe;
              return pipe;
            }
            function addOneToPipe() {
              return pipe + 1;
            }
            function simplePipeline(i) {
              i into addOneToPipe()
              into printPipe()
              into addOneToPipe()
              into printPipe();
            }

            simplePipeline(5);
          """
simple2 = """
            function printAndAdd() {
              print pipe;
              return pipe + 1;
            }
            loop(let i = 0; i < 5; i = i into printAndAdd();) {
              pass;
            }
          """
simple3 = """
            function addOne() {
              return pipe + 1;
            }
            let a = 1;

            if ((a + 1) == a into addOne()) {
              print "Yes!";
            } else {
              print "No!";
            }
          """
simple4 = """
            function isTrue() {
              return pipe == True;
            }
            if ((3 < 5) into isTrue()) {
              print 0;
            } else {
              print 1;
            }
            if ((not (3 > 5)) into isTrue()) {
              print 0;
            } else {
              print 1;
            }
          """

class PipeTest(BaseTestCase):
  def test_simple0(self):
    self.assert_stdout(simple0, '1\n')

  def test_simple1(self):
    self.assert_stdout(simple1, '6\n7\n')

  def test_simple2(self):
    self.assert_stdout(simple2, '0\n1\n2\n3\n4\n')

  def test_simple3(self):
    self.assert_stdout(simple3, 'Yes!\n')

  def test_simple4(self):
    self.assert_stdout(simple4, '0\n0\n')

if __name__ == '__main__':
  unittest.main()