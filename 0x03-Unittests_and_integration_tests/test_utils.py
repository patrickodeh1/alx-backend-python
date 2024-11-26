#!/usr/bin/env python3
"""test"""
import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from utils import access_nested_map


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


if __name__ == "__main__":
    unittest.main()
