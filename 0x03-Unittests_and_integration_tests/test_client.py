#!/usr/bin/env python3
"""Test suite for the GithubOrgClient class"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch('client.get_json', return_value={"repos_url": "mocked_repos_url"})
    def test_org(self, org_name, expected_return, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""

        # Create an instance of GithubOrgClient
        client = GithubOrgClient(org_name)

        # Call the org property
        result = client.org

        # Ensure get_json is called once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Check that the org method returns the expected result
        self.assertEqual(result, {"repos_url": "mocked_repos_url"})


if __name__ == "__main__":
    unittest.main()
