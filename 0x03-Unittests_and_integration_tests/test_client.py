#!/usr/bin/env python3
"""Test suite for the GithubOrgClient class"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock
from client import GithubOrgClient


from parameterized import parameterized

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"})
    ])
    @patch('client.GithubOrgClient._public_repos_url', return_value="https://api.github.com/orgs/mock-org/repos")
    @patch('client.GithubOrgClient.get_json')
    def test_public_repos(self, mock_get_json, mock_public_repos_url):
        """Test the public_repos method works properly"""

        # Define the mocked payload returned by get_json
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "my_license"}},
            {"name": "repo2", "license": {"key": "other_license"}}
        ]

        # Create an instance of GithubOrgClient
        client = GithubOrgClient("mock-org")

        # Call the public_repos method with a license filter
        result = client.public_repos(license="my_license")

        # Test the result
        self.assertEqual(result, ["repo1"])

        # Ensure get_json was called once with the expected URL
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/mock-org/repos")

        # Ensure _public_repos_url was accessed
        mock_public_repos_url.assert_called_once()

    @patch('client.GithubOrgClient.org', return_value={'repos_url': 'https://api.github.com/orgs/mock-org/repos'})
    def test_public_repos_url(self, mock_org):
        """Test that the _public_repos_url property works correctly"""

        # Create an instance of GithubOrgClient
        client = GithubOrgClient("mock-org")

        # Test that the _public_repos_url property returns the correct value
        self.assertEqual(client._public_repos_url, 'https://api.github.com/orgs/mock-org/repos')

        # Ensure org was accessed correctly
        mock_org.assert_called_once()


    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test the public_repos method works properly
        """

        # Define the mocked payload returned by get_json
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "my_license"}},
            {"name": "repo2", "license": {"key": "other_license"}},
            {"name": "repo3", "license": {"key": "my_license"}}
        ]

        # Mock the _public_repos_url property using patch as a context manager
        with patch('client.GithubOrgClient._public_repos_url',
                   return_value="https://api.github.com/orgs/mock-org/repos"):
            # Create an instance of GithubOrgClient
            client = GithubOrgClient("mock-org")

            # Call the public_repos method with a license filter
            result = client.public_repos(license="my_license")

            self.assertEqual(result, ["repo1", "repo3"])

            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/mock-org/repos")

            # Ensure that _public_repos_url was accessed once
            self.assertTrue(client._public_repos_url)

    
if __name__ == "__main__":
    unittest.main()
