import unittest
from unittest.mock import patch, MagicMock
import math

# Import the Quantity class from its module
from healthchain.models.data.concept import Quantity


class TestQuantity(unittest.TestCase):

    @patch('healthchain.models.data.concept.logging')
    def test_content_none(self, mock_logging):
        """Test that content can be None."""
        quantity = Quantity(content=None)
        self.assertIsNone(quantity.content)
        mock_logging.error.assert_not_called()

    @patch('healthchain.models.data.concept.logging')
    def test_content_float(self, mock_logging):
        """Test that valid float content is accepted."""
        quantity = Quantity(content=123.45)
        self.assertEqual(quantity.content, 123.45)
        mock_logging.error.assert_not_called()

    @patch('healthchain.models.data.concept.logging')
    def test_content_infinite_float(self, mock_logging):
        """Test that infinite float content raises OverflowError."""
        with self.assertRaises(OverflowError):
            Quantity(content=float('inf'))
        mock_logging.error.assert_called_once_with(
            "OverflowError: The value 'inf' is too large."
        )

    @patch('healthchain.models.data.concept.logging')
    def test_content_valid_str_float(self, mock_logging):
        """Test that valid string representing float is accepted."""
        quantity = Quantity(content='123.45')
        self.assertEqual(quantity.content, 123.45)
        mock_logging.error.assert_not_called()

    @patch('healthchain.models.data.concept.logging')
    def test_content_invalid_str(self, mock_logging):
        """Test that invalid string raises ValueError."""
        with self.assertRaises(ValueError):
            Quantity(content='abc')
        mock_logging.error.assert_called_once_with(
            "ValueError: Unable to convert 'abc' to float."
        )

    @patch('healthchain.models.data.concept.logging')
    def test_content_infinite_str(self, mock_logging):
        """Test that string representing infinity raises OverflowError."""
        with self.assertRaises(OverflowError):
            Quantity(content='inf')
        mock_logging.error.assert_called_once_with(
            "OverflowError: The value 'inf' is too large."
        )

    @patch('healthchain.models.data.concept.logging')
    def test_content_unsupported_type(self, mock_logging):
        """Test that unsupported types raise TypeError."""
        with self.assertRaises(TypeError):
            Quantity(content=[1, 2, 3])
        mock_logging.error.assert_not_called()

    @patch('healthchain.models.data.concept.logging')
    def test_scale_field(self, mock_logging):
        """Test that scale field accepts string values."""
        quantity = Quantity(scale='kg')
        self.assertEqual(quantity.scale, 'kg')
        mock_logging.error.assert_not_called()

    @patch('healthchain.models.data.concept.logging')
    def test_scale_field_none(self, mock_logging):
        """Test that scale field can be None."""
        quantity = Quantity(scale=None)
        self.assertIsNone(quantity.scale)
        mock_logging.error.assert_not_called()

    @patch('healthchain.models.data.concept.logging')
    def test_full_valid_data(self, mock_logging):
        """Test that Quantity accepts full valid data."""
        quantity = Quantity(content='99.99', scale='kg')
        self.assertEqual(quantity.content, 99.99)
        self.assertEqual(quantity.scale, 'kg')
        mock_logging.error.assert_not_called()

    @patch('healthchain.models.data.concept.logging')
    def test_large_float_value(self, mock_logging):
        """Test that very large float values are handled."""
        large_value = 1e308  # Near the maximum float value
        quantity = Quantity(content=large_value)
        self.assertEqual(quantity.content, large_value)
        mock_logging.error.assert_not_called()

    @patch('healthchain.models.data.concept.logging')
    def test_negative_infinite_float(self, mock_logging):
        """Test that negative infinity raises OverflowError."""
        with self.assertRaises(OverflowError):
            Quantity(content=float('-inf'))
        mock_logging.error.assert_called_once_with(
            "OverflowError: The value '-inf' is too large."
        )

    @patch('healthchain.models.data.concept.logging')
    def test_content_with_whitespace_string(self, mock_logging):
        """Test that strings with whitespace are handled."""
        quantity = Quantity(content='  42.0  ')
        self.assertEqual(quantity.content, 42.0)
        mock_logging.error.assert_not_called()

    @patch('healthchain.models.data.concept.logging')
    def test_content_with_comma_string(self, mock_logging):
        """Test that strings with commas raise ValueError."""
        with self.assertRaises(ValueError):
            Quantity(content='1,000')
        mock_logging.error.assert_called_once_with(
            "ValueError: Unable to convert '1,000' to float."
        )

    @patch('healthchain.models.data.concept.logging')
    def test_content_nan(self, mock_logging):
        """Test that NaN values are accepted."""
        nan_value = float('nan')
        quantity = Quantity(content=nan_value)
        self.assertTrue(math.isnan(quantity.content))
        mock_logging.error.assert_not_called()

    @patch('healthchain.models.data.concept.logging')
    def test_content_negative_number(self, mock_logging):
        """Test that negative numbers are accepted."""
        quantity = Quantity(content=-123.45)
        self.assertEqual(quantity.content, -123.45)
        mock_logging.error.assert_not_called()


# If this script is run directly, run the tests
if __name__ == '__main__':
    unittest.main()
