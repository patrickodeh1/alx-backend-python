#!/usr/bin/env python3
"""
test suite for utils.py
"""
import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test suite for the access_nested_map function"""
    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a", "b"], 2),
        ({"a": {"b": {"c": 3}}}, ["a", "b", "c"], 3),
    ])
    def test_access_nested_map(self, nested_map:
                               Mapping, path: Sequence, expected: Any):
        """Test that the function returns the correct value"""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({"a": 1}, ["b"]),
        ({"a": {"b": 2}}, ["a", "c"]),
    ])
    def test_access_nested_map_exception(self, nested_map:
                                         Mapping, path: Sequence):
        """Test that the function raises a KeyError for missing keys"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test suite for the get_json function"""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """Test that get_json returns the expected result"""

        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)

            self.assertEqual(result, test_payload)

            mock_get.reset_mock()


class TestMemoize(unittest.TestCase):
    """Test suite for the memoize decorator"""

    def test_memoize(self):
        """Test that memoize caches the result of a method"""

        class TestClass:
            """Class to test the memoize decorator"""

            def a_method(self):
                """A simple method"""
                return 42

            @memoize
            def a_property(self):
                """A property decorated with memoize"""
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) \
                as mock_method:
            test_instance = TestClass()

            # Call the memoized property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Assert the result is correct both times
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure the method is called only once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
