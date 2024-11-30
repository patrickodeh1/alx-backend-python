#!/usr/bin/env python3
"""Test suite for the GithubOrgClient class"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient"""

    @patch('client.GithubOrgClient.org')
    def test_public_repos_url(self, mock_org):
        """Test that the _public_repos_url property works correctly"""

        # Mocking the return value of the org method
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/mock-org/repos"}

        # Create an instance of GithubOrgClient
        client = GithubOrgClient("mock-org")

        # Test that the _public_repos_url property returns the correct value
        self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/mock-org/repos")

        # Ensure that the org method was called once to retrieve the repos_url
        mock_org.assert_called_once()

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', return_value="https://api.github.com/orgs/mock-org/repos")
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """Test the public_repos method"""

        # Mock the payload returned by get_json
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "my_license"}},
            {"name": "repo2", "license": {"key": "other_license"}}
        ]

        # Create an instance of GithubOrgClient
        client = GithubOrgClient("mock-org")

        # Call the public_repos method
        result = client.public_repos(license="my_license")

        # Check that the result matches the expected list of repos
        self.assertEqual(result, ["repo1"])

        # Ensure that get_json was called once with the correct URL
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/mock-org/repos")

        # Ensure that the _public_repos_url property was accessed once
        mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Test the has_license method"""

        result = GithubOrgClient.has_license(repo, license_key)

        self.assertEqual(result, expected_result)


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test suite for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up patchers and mock data"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop patchers"""
        cls.get_patcher.stop()

    @parameterized_class([
        {"org_payload": org_payload, "repos_payload": repos_payload, "expected_repos": expected_repos},
        {"org_payload": apache2_repos, "repos_payload": repos_payload, "expected_repos": expected_repos},
    ])
    def test_public_repos_integration(self):
        """Test the public_repos method in an integration test"""

        # Mocking the requests.get to return the respective payloads
        self.mock_get.side_effect = [
            Mock(json=lambda: self.org_payload),
            Mock(json=lambda: self.repos_payload)
        ]

        # Create an instance of GithubOrgClient
        client = GithubOrgClient("mock-org")

        # Test that the public_repos method returns the correct repos
        result = client.public_repos()

        self.assertEqual(result, self.expected_repos)

        # Ensure requests.get was called twice (once for the org, once for repos)
        self.mock_get.assert_called()

    def test_repos_payload(self):
        """Test that repos_payload is correctly returned"""
        pass


if __name__ == "__main__":
    unittest.main()
