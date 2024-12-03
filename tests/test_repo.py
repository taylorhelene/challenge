import os
import shutil
from src.repo import Repository

def setup_module(module):
    """Create a clean environment for tests."""
    if os.path.exists("test_repo"):
        shutil.rmtree("test_repo")

def teardown_module(module):
    """Clean up after tests."""
    if os.path.exists("test_repo"):
        shutil.rmtree("test_repo")

def test_create_repo():
    repo = Repository("test_repo")
    repo.create_repo()
    # Check if repository structure exists
    assert os.path.exists("test_repo/.vcs")
    assert os.path.exists("test_repo/.vcs/history.json")
    assert os.path.exists("test_repo/.vcs/staged.json")
    assert os.path.exists("test_repo/.vcs/branches.json")
    assert os.path.exists("test_repo/.vcs/.vcsignore")
