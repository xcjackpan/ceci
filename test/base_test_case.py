import io
import sys
import unittest
import unittest.mock
from contextlib import redirect_stdout
from unnamed.unnamed import run_test

class BaseTestCase(unittest.TestCase):
  @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
  def assert_stdout(self, test_case, expected_output, mock_stdout):
    f = io.StringIO()
    with redirect_stdout(f):
      run_test(test_case)
    out = f.getvalue()
    self.assertEqual(out, expected_output)

  def assert_exception(self, test_case, expected_exception):
    self.assertRaises(expected_exception, run_test, test_case)
