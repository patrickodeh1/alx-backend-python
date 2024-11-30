#!/usr/bin/env python3
"""test"""
import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json


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
        
        # Define test cases
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
        
        for test_url, test_payload in test_cases:
            # Configure the mock to return the test payload
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call the function with the test URL
            result = get_json(test_url)

            # Verify the mock was called exactly once with the correct arguments
            mock_get.assert_called_once_with(test_url)

            # Assert that the function returns the expected result
            self.assertEqual(result, test_payload)

            # Reset the mock for the next iteration
            mock_get.reset_mock()


if __name__ == "__main__":
    unittest.main()
