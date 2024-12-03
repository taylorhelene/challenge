import os
import unittest
from src.repo import Repository

class TestRepositoryAdd(unittest.TestCase):
    def setUp(self):
        self.repo_name = "test_repo"
        self.repo = Repository(self.repo_name)
        self.repo.create_repo()

    def test_add_file(self):
        test_file = "test_file.txt"
        with open(test_file, 'w') as f:
            f.write("Test content")
        
        self.repo.add(test_file)
        staged_files = self.repo._get_staged_files()
        self.assertIn(test_file, staged_files)

    def test_add_non_existent_file(self):
        with self.assertRaises(Exception):
            self.repo.add("non_existent_file.txt")

if __name__ == "__main__":
    unittest.main()
