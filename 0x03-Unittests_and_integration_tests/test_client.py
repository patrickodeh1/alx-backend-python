import unittest
from unittest.mock import patch

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    def test_public_repos(self):
        """Test public_repos method with and without license filter"""

        # Mock get_json and repos_payload to avoid real API calls
        with patch.object(GithubOrgClient, 'repos_payload') as mock_repos_payload:
            # Define expected repos payload
            expected_payload = [
                {"name": "repo1", "license": {"key": "mit"}},
                {"name": "repo2", "license": {"key": "apache-2.0"}},
                {"name": "repo3", "license": None}
            ]

            # Set mock_repos_payload to return the expected data
            mock_repos_payload.return_value = expected_payload

            # Create an instance of GithubOrgClient
            client = GithubOrgClient("some-org")

            # Test without license filter
            all_repos = client.public_repos()
            self.assertEqual(all_repos, ["repo1", "repo2"])

            # Test with license filter
            filtered_repos = client.public_repos(license="mit")
            self.assertEqual(filtered_repos, ["repo1"])

            # Verify that repos_payload was called once
            mock_repos_payload.assert_called_once()


if __name__ == '__main__':
    unittest.main()