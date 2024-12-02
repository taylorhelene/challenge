import os
import json
from datetime import datetime
from src.repo import Repository
from src.ui import display_welcome_message, show_error, show_success

def init_repo(repo_name):
    repo = Repository(repo_name)
    repo.create_repo()
    show_success(f"Repository '{repo_name}' initialized successfully!")

def add_to_stage(repo_name, file_name):
    repo = Repository(repo_name)
    repo.add(file_name)
    show_success(f"File '{file_name}' added to the staging area.")

def commit_changes(repo_name, message):
    repo = Repository(repo_name)
    repo.commit(message)
    show_success(f"Commit made with message: {message}")

def create_branch(repo_name, branch_name):
    repo = Repository(repo_name)
    repo.create_branch(branch_name)
    show_success(f"Branch '{branch_name}' created.")

def show_commit_history(repo_name):
    repo = Repository(repo_name)
    history = repo.view_commit_history()
    for commit in history:
        print(f"Commit: {commit['message']} at {commit['date']}")

def clone_repo(repo_name, new_name):
    repo = Repository(repo_name)
    repo.clone(new_name)
    show_success(f"Repository '{repo_name}' cloned to '{new_name}'.")

def run():
    display_welcome_message()

    # Sample commands
    init_repo("test_repo")
    add_to_stage("test_repo", "file1.txt")
    commit_changes("test_repo", "Initial commit")
    create_branch("test_repo", "dev")
    show_commit_history("test_repo")
    clone_repo("test_repo", "cloned_repo")

if __name__ == "__main__":
    run()
