import os
import json
from datetime import datetime
from shutil import copytree, rmtree

class Repository:
    def __init__(self, name):
        self.name = name
        self.repo_dir = os.path.join(name, ".vcs")
        self.history_file = os.path.join(self.repo_dir, "history.json")
        self.stage_file = os.path.join(self.repo_dir, "staged.json")
        self.branch_file = os.path.join(self.repo_dir, "branches.json")
        self.ignore_file = os.path.join(self.repo_dir, ".vcsignore")

    def create_repo(self):
        if not os.path.exists(self.repo_dir):
            os.makedirs(self.repo_dir)
            with open(self.history_file, 'w') as f:
                json.dump([], f)
            with open(self.stage_file, 'w') as f:
                json.dump([], f)
            with open(self.branch_file, 'w') as f:
                json.dump({"main": []}, f)
            open(self.ignore_file, 'w').close()
        else:
            raise Exception("Repository already exists!")

    def add(self, file_name):
        with open(self.stage_file, 'r+') as f:
            staged = json.load(f)
            staged.append(file_name)
            f.seek(0)
            json.dump(staged, f, indent=4)

    def commit(self, message):
        with open(self.stage_file, 'r') as f:
            staged = json.load(f)

        with open(self.history_file, 'r+') as f:
            history = json.load(f)
            commit = {
                "message": message,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "files": staged,
            }
            history.append(commit)
            f.seek(0)
            json.dump(history, f, indent=4)

        with open(self.stage_file, 'w') as f:
            json.dump([], f)

    def create_branch(self, branch_name):
        with open(self.branch_file, 'r+') as f:
            branches = json.load(f)
            if branch_name in branches:
                raise Exception("Branch already exists!")
            branches[branch_name] = []
            f.seek(0)
            json.dump(branches, f, indent=4)

    def view_commit_history(self):
        with open(self.history_file, 'r') as f:
            return json.load(f)

    def clone(self, new_name):
        if os.path.exists(new_name):
            raise Exception("Target directory already exists!")
        copytree(self.name, new_name)
