import unittest
from plpipe.plpipe_core import Field
import numpy as np
import os


class TestFieldMethods(unittest.TestCase):

    def setUp(self):
        # Create a sample Field object for testing
        self.field = Field(name="Test Field", x=np.array([1, 2, 3]), y=np.array([
                           4, 5]), v=np.array([[10, 20, 30], [40, 50, 60]]).T)

    def test_interpolate(self):
        # Test if interpolate returns a Field object with interpolated values
        interpolated_field = self.field.interpolate([1.5, 2.5, 3.5], [4.5, -5.5])

    def test_transpose(self):
        # Test if transpose returns a Field object with transposed values
        transposed_field = self.field.transpose()
        # Add assertions here to check the transposed_field attributes
        self.assertEqual(list(self.field._x), list(transposed_field._y))
        self.assertEqual(list(self.field._y), list(transposed_field._x))
        self.assertTrue(np.all(self.field._v == transposed_field._v.T))

    def test_write_data(self):
        expected_output = """#Test Field      4.00000000      5.00000000 
     1.00000000     10.00000000     40.00000000 
     2.00000000     20.00000000     50.00000000 
     3.00000000     30.00000000     60.00000000 
"""  # Define the expected multi-line output

        # Create a temporary file for testing
        temp_file = '/tmp/test-%010d' % np.random.randint(100000)
        with open(temp_file, 'w') as f:
            self.field.write_data(f)

        # Check if the content of the file matches the expected output
        with open(temp_file, 'r') as f:
            actual_output = f.read()

        self.assertEqual(actual_output, expected_output)

        os.remove(temp_file)

    def test_field_plot(self):
        os.makedirs('./tests/output/', exist_ok=True)
        temp_file = './tests/output/test-field-plot'
        self.field.print_field_img(filename=temp_file)

    def test_field_plot_cli(self):
        print()
        self.field.set_data(name="Updated Field", x=np.array([7, 8, 9]), y=np.array([
                            6, 7]), v=np.array([[0, 1, 0], [1, 2, 100]]))
        self.field.print_int_field_cli(labels=['a', 'b', 'c', 'd'])

    def test_strip_plot(self):
        self.field.set_data(name="Test Field", x=np.array([1, 2, 3]), y=np.array([
            4, 5]), v=np.array([[10, 29.4, 30], [40, 89.1, 60]]).T)
        os.makedirs('./tests/output/', exist_ok=True)
        temp_file = './tests/output/test-strip-plot'
        self.field.print_strips(filename=temp_file)

    def test_strip_plot_no_y(self):
        self.field.set_data(name="Test Field", x=np.array(
            [1, 2, 3]), v=np.array([[10, 29.4, 30], [40, 89.1, 60]]).T)
        os.makedirs('./tests/output/', exist_ok=True)
        temp_file = './tests/output/test-strip-plot-no-y'
        self.field.print_strips(filename=temp_file)


if __name__ == '__main__':
    unittest.main()
