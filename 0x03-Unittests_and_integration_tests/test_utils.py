#!/usr/bin/env python3
"""
Unit tests for utils module
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test cases for access_nested_map function
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test normal inputs"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError, 'a'),
        ({"a": 1}, ("a", "b"), KeyError, 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path,
                                        exception, expected_msg):
        """Test exception cases"""
        with self.assertRaises(exception) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected_msg}'")


class TestGetJson(unittest.TestCase):
    """
    Test cases for get_json function
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns correct data"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response
        
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test cases for memoize decorator
    """
    def test_memoize(self):
        """Test memoization functionality"""
        class TestClass:
            """Test class for memoization"""
            def a_method(self):
                return 42
            
            @memoize
            def a_property(self):
                return self.a_method()
        
        with patch.object(TestClass, 'a_method', 
                          return_value=42) as mock_method:
            test_obj = TestClass()
            self.assertEqual(test_obj.a_property, 42)
            self.assertEqual(test_obj.a_property, 42)
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()