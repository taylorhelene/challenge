import os
import json
from datetime import datetime

class Repository:
    def __init__(self, name):
        self.name = name
        self.repo_dir = f"./{self.name}/.vcs"
        self.history_file = f"{self.repo_dir}/history.json"

    def create_repo(self):
        if not os.path.exists(self.repo_dir):
            os.makedirs(self.repo_dir)
            with open(self.history_file, 'w') as f:
                json.dump([], f)
        else:
            raise Exception("Repository already exists!")

    def add(self, file_name):
        with open(f"{self.repo_dir}/staged_files.json", 'a') as f:
            f.write(f"{file_name}\n")

    def commit(self, message):
        with open(self.history_file, 'r+') as f:
            history = json.load(f)
            commit = {
                "message": message,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            history.append(commit)
            f.seek(0)
            json.dump(history, f, indent=4)

    def create_branch(self, branch_name):
        # Simulating branch creation by adding it to a file
        with open(f"{self.repo_dir}/branches.json", 'a') as f:
            f.write(f"{branch_name}\n")

    def view_commit_history(self):
        with open(self.history_file, 'r') as f:
            return json.load(f)

    def clone(self, new_name):
        # Simulating repo cloning by copying files
        os.makedirs(new_name)
        os.makedirs(f"{new_name}/.vcs")
        with open(f"{new_name}/.vcs/history.json", 'w') as f:
            json.dump([], f)
