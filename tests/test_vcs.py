import os
import json
import unittest
import shutil
from src.repo import Repository


class TestRepository(unittest.TestCase):
    TEST_REPO = "test_repo"

    def setUp(self):
        """Set up a clean environment for each test."""
        if os.path.exists(self.TEST_REPO):
            shutil.rmtree(self.TEST_REPO)
        self.repo = Repository(self.TEST_REPO)
        self.repo.create_repo()

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.TEST_REPO):
            shutil.rmtree(self.TEST_REPO)

    def test_create_repo(self):
        """Test repository initialization."""
        self.assertTrue(os.path.exists(self.repo.repo_dir))
        self.assertTrue(os.path.exists(self.repo.history_file))
        self.assertTrue(os.path.exists(self.repo.stage_file))
        self.assertTrue(os.path.exists(self.repo.branch_file))
        self.assertTrue(os.path.exists(self.repo.ignore_file))

    def test_add_file(self):
        """Test adding a file to staging."""
        test_file = os.path.join(self.TEST_REPO, ".vcs", "test.txt")
        os.makedirs(os.path.dirname(test_file), exist_ok=True)  # Ensure .vcs directory exists
        with open(test_file, "w") as f:
            f.write("This is a test file.")

        self.repo.add("test.txt")

        with open(self.repo.stage_file, "r") as f:
            staged_files = json.load(f)
        self.assertIn("test.txt", staged_files)

    def test_commit(self):
        """Test committing staged files."""
        test_file = os.path.join(self.TEST_REPO, ".vcs", "test.txt")
        os.makedirs(os.path.dirname(test_file), exist_ok=True)  # Ensure .vcs directory exists
        with open(test_file, "w") as f:
            f.write("This is a test file.")

        self.repo.add("test.txt")
        self.repo.commit("Initial commit")

        with open(self.repo.history_file, "r") as f:
            history = json.load(f)

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["message"], "Initial commit")

    def test_create_branch(self):
        """Test branch creation."""
        self.repo.create_branch("new_branch")
        with open(self.repo.branch_file, "r") as f:
            branches = json.load(f)
        self.assertIn("new_branch", branches)

    def test_merge(self):
        """Test merging branches."""
        self.repo.create_branch("new_branch")
        with open(self.repo.branch_file, "r") as f:
            branches = json.load(f)
        self.repo.merge("new_branch")
        self.assertIn("new_branch", branches)

    def test_diff(self):
        """Test viewing differences between branches."""
        self.repo.create_branch("new_branch")
        diff = self.repo.diff("new_branch")
        self.assertIn("No differences", diff)

    def test_ignore(self):
        """Test ignoring files."""
        self.repo.ignore("ignored_file.txt")
        ignore_list = self.repo.view_ignore_list()
        self.assertIn("ignored_file.txt", ignore_list)


if __name__ == "__main__":
    unittest.main()
