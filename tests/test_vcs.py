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
        self.assertTrue(os.path.exists(self.repo.repo_dir))

    def test_add_commit_branch_diff(self):
        with open(os.path.join(self.TEST_REPO, "main.txt"), "w") as f:
            f.write("Hello Main")
        self.repo.add("main.txt")
        self.repo.commit("Add main.txt")
        self.repo.create_branch("feature_branch")
        self.repo.switch_branch("feature_branch")
        with open(os.path.join(self.TEST_REPO, "feature.txt"), "w") as f:
            f.write("Feature branch content")
        self.repo.add("feature.txt")
        self.repo.commit("Add feature.txt")
        self.repo.switch_branch("main")
        diff = self.repo.diff("feature_branch")
        self.assertIn("feature.txt", diff)

    def test_ignore_files(self):
        self.repo.ignore("ignore_me.txt")
        self.assertIn("ignore_me.txt", self.repo.view_ignore_list())

    def test_merge_branch(self):
        self.repo.create_branch("branch_a")
        self.repo.switch_branch("branch_a")
        with open(os.path.join(self.TEST_REPO, "file_a.txt"), "w") as f:
            f.write("Content A")
        self.repo.add("file_a.txt")
        self.repo.commit("Add file_a.txt")
        self.repo.switch_branch("main")
        self.repo.merge("branch_a")
        history = self.repo.view_commit_history()
        self.assertTrue(any("file_a.txt" in c["files"] for c in history))

if __name__ == "__main__":
    unittest.main()
