#!/usr/bin/env python3
"""Test suite for the GithubOrgClient class"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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

    @patch('client.GithubOrgClient.org')
    def test_public_repos_url(self, mock_org):
        """Test that the _public_repos_url property works correctly"""

        # Mock the return value of the org method to simulate the API response
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/mock-org/repos"}

        # Create an instance of GithubOrgClient
        client = GithubOrgClient("mock-org")

        # Test that the _public_repos_url property returns the correct value
        self.assertEqual(client._public_repos_url,
                         "https://api.github.com/orgs/mock-org/repos")

        # Ensure that the org method was called once to retrieve the repos_url
        mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method"""

        # Define the mocked payload returned by get_json
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "my_license"}},
            {"name": "repo2", "license": {"key": "other_license"}},
            {"name": "repo3", "license": {"key": "my_license"}},
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
