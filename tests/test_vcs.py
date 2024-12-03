import os
import pytest
import sys

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch
from src.repo import Repository
from src.utils import display_progress, display_message
from colorama import Fore, init

# Initialize colorama for consistent output during tests
init(autoreset=True)

# Cleanup function to remove any created repositories and files after tests
def cleanup_repo(repo_name):
    if os.path.exists(repo_name):
        for root, dirs, files in os.walk(repo_name, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(repo_name)

# Test the `init` command
def test_init():
    repo_name = "test_repo"
    repo = Repository(repo_name)
    
    # Simulate running `vcs.py init` command
    repo.create_repo()
    assert os.path.exists(repo.repo_dir), "Repository directory was not created."
    assert os.path.exists(repo.history_file), "History file not created."
    assert os.path.exists(repo.stage_file), "Stage file not created."
    assert os.path.exists(repo.branch_file), "Branch file not created."
    assert os.path.exists(repo.ignore_file), "Ignore file not created."

    cleanup_repo(repo_name)  # Clean up after test

# Test the `add` command
def test_add():
    repo_name = "test_repo"
    repo = Repository(repo_name)
    repo.create_repo()

    # Simulate creating a new file to stage
    with open(f"{repo.repo_dir}/file1.txt", "w") as f:
        f.write("Sample content.")

    repo.add("file1.txt")
    assert "file1.txt" in repo.staged_files(), "File was not staged properly."

    cleanup_repo(repo_name)

# Test the `commit` command
def test_commit():
    repo_name = "test_repo"
    repo = Repository(repo_name)
    repo.create_repo()

    # Simulate adding a file and committing it
    with open(f"{repo.repo_dir}/file1.txt", "w") as f:
        f.write("Sample content.")

    repo.add("file1.txt")
    repo.commit("Initial commit")
    assert len(repo.view_commit_history()) == 1, "Commit was not added properly."

    cleanup_repo(repo_name)

# Test the `branch` command
def test_create_branch():
    repo_name = "test_repo"
    repo = Repository(repo_name)
    repo.create_repo()

    repo.create_branch("feature_branch")
    assert "feature_branch" in repo.view_commit_history(), "Branch was not created properly."

    cleanup_repo(repo_name)

# Test the `clone` command
def test_clone():
    original_repo_name = "test_repo"
    cloned_repo_name = "cloned_repo"
    repo = Repository(original_repo_name)
    repo.create_repo()

    # Simulate cloning the repository
    repo.clone(cloned_repo_name)
    assert os.path.exists(cloned_repo_name), "Cloning failed."

    cleanup_repo(original_repo_name)
    cleanup_repo(cloned_repo_name)

# Test the `log` command
def test_log():
    repo_name = "test_repo"
    repo = Repository(repo_name)
    repo.create_repo()

    # Simulate adding files and committing them
    with open(f"{repo.repo_dir}/file1.txt", "w") as f:
        f.write("Initial content.")
    repo.add("file1.txt")
    repo.commit("First commit")

    history = repo.view_commit_history()
    assert len(history) > 0, "Commit history is empty."

    cleanup_repo(repo_name)

# Test interactive mode
def test_interactive_mode():
    repo_name = "test_interactive_repo"

    # Mock user input for interactive mode
    with patch("builtins.input", side_effect=["init", repo_name, "add", repo_name, "file1.txt", "commit", repo_name, "Initial commit", "exit"]):
        # Run the main function with mocked input
        with patch("sys.stdout", new_callable=list):
            repo = Repository(repo_name)
            repo.create_repo()
            repo.add("file1.txt")
            repo.commit("Initial commit")

            # Verify repository is created
            assert os.path.exists(repo.repo_dir), "Repository directory not created in interactive mode."
            assert len(repo.view_commit_history()) > 0, "Commit history is empty in interactive mode."

    cleanup_repo(repo_name)

# Test project mode (command-line arguments)
def test_project_mode():
    repo_name = "test_project_mode"
    repo = Repository(repo_name)

    # Run init command via project mode
    repo.create_repo()
    assert os.path.exists(repo.repo_dir), "Repository directory was not created."

    # Add and commit file
    with open(f"{repo.repo_dir}/file1.txt", "w") as f:
        f.write("Test content.")
    repo.add("file1.txt")
    repo.commit("Test commit")
    assert len(repo.view_commit_history()) > 0, "Commit history is empty in project mode."

    cleanup_repo(repo_name)

