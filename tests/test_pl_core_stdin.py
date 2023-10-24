import unittest
from unittest import mock
from io import StringIO
import numpy as np
from plpipe.plpipe_core import parse_stdin

mock


def check_field(field, x, y, v):
    """Check that a field is as expected

    :field: TODO
    :x: TODO
    :y: TODO
    :v: TODO
    :returns: TODO

    """
    if x is not None:
        np.testing.assert_array_equal(field._x, x)
    if y is not None:
        np.testing.assert_array_equal(field._y, y)
    if v is not None:
        np.testing.assert_array_equal(field._v, v)


class TestParseStdin(unittest.TestCase):
    def test_parse_stdin(self):
        # Sample data to simulate stdin
        sample_data = """####Vaxis
###Yaxis
##Xaxis
#TestField      4.00000000      5.00000000
     1.00000000     10.00000000     40.00000000
     2.00000000     20.00000000     50.00000000
     3.00000000     30.00000000     60.00000000
#TestField2      4.00000000      5.00000000
     4.00000000     9.00000000     39.00000000
     2.10000000     20.10000000     52.00000000
     3.30000000     -30.00000000     61.00000000
"""  # Define the expected multi-line output

        # Create a StringIO object to simulate stdin
        fake_stdin = StringIO(sample_data)

        # Patch sys.stdin with the StringIO object
        with unittest.mock.patch('sys.stdin', fake_stdin):
            result = parse_stdin()

        check_field(result._fields[0],
                    [1., 2., 3.],
                    [4., 5.],
                    [[10., 40.], [20., 50.], [30., 60.]])
        check_field(result._fields[1],
                    [4., 2.1, 3.3],
                    [4., 5.],
                    [[9., 39.], [20.1, 52.], [-30., 61.]])

    def test_parse_stdin_no_yaxis(self):
        # Sample data to simulate stdin
        sample_data = """####Vaxis
##Xaxis
#TestField      4.00000000      5.00000000
     1.00000000     10.00000000     40.00000000
     2.00000000     20.00000000     50.00000000
     3.00000000     30.00000000     60.00000000
"""  # Define the expected multi-line output

        # Create a StringIO object to simulate stdin
        fake_stdin = StringIO(sample_data)

        # Patch sys.stdin with the StringIO object
        with unittest.mock.patch('sys.stdin', fake_stdin):
            result = parse_stdin()

        check_field(result._fields[-1],
                    [1., 2., 3.],
                    [4., 5.],
                    [[10., 40.], [20., 50.], [30., 60.]])

    def test_parse_stdin_no_vaxis_no_yaxis(self):
        # Sample data to simulate stdin
        sample_data = """##Xaxis
#TestField      4.00000000      5.00000000
     1.00000000     10.00000000     40.00000000
     2.00000000     20.00000000     50.00000000
     3.00000000     30.00000000     60.00000000
"""  # Define the expected multi-line output

        # Create a StringIO object to simulate stdin
        fake_stdin = StringIO(sample_data)

        # Patch sys.stdin with the StringIO object
        with unittest.mock.patch('sys.stdin', fake_stdin):
            result = parse_stdin()

        check_field(result._fields[-1],
                    [1., 2., 3.],
                    [4., 5.],
                    [[10., 40.], [20., 50.], [30., 60.]])

    def test_parse_stdin_no_vaxis_no_yaxis_no_xaxis(self):
        # Sample data to simulate stdin
        sample_data = """#TestField      4.00000000      5.00000000
     1.00000000     10.00000000     40.00000000
     2.00000000     20.00000000     50.00000000
     3.00000000     30.00000000     60.00000000
"""  # Define the expected multi-line output

        # Create a StringIO object to simulate stdin
        fake_stdin = StringIO(sample_data)

        # Patch sys.stdin with the StringIO object
        with unittest.mock.patch('sys.stdin', fake_stdin):
            result = parse_stdin()

        check_field(result._fields[-1],
                    [1., 2., 3.],
                    [4., 5.],
                    [[10., 40.], [20., 50.], [30., 60.]])

    def test_parse_stdin_no_labels(self):
        # Sample data to simulate stdin
        sample_data = """1.00000000     10.00000000     40.00000000
     2.00000000     20.00000000     50.00000000
     3.00000000     30.00000000     60.00000000
"""  # Define the expected multi-line output

        # Create a StringIO object to simulate stdin
        fake_stdin = StringIO(sample_data)

        # Patch sys.stdin with the StringIO object
        with unittest.mock.patch('sys.stdin', fake_stdin):
            result = parse_stdin()

        check_field(result._fields[-1],
                    [1., 2., 3.],
                    None,
                    [[10., 40.], [20., 50.], [30., 60.]])


if __name__ == '__main__':
    unittest.main()
