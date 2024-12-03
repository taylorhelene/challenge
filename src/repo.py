import os
import json
from datetime import datetime
from shutil import copytree, rmtree
from difflib import unified_diff

class Repository:
    def __init__(self, name):
        self.name = name
        self.repo_dir = os.path.join(name, ".vcs")
        self.history_file = os.path.join(self.repo_dir, "history.json")
        self.stage_file = os.path.join(self.repo_dir, "staged.json")
        self.branch_file = os.path.join(self.repo_dir, "branches.json")
        self.ignore_file = os.path.join(self.repo_dir, ".vcsignore")
        self._load_ignore_list()

    def _load_ignore_list(self):
        """Load files that should be ignored from .vcsignore."""
        if os.path.exists(self.ignore_file):
            with open(self.ignore_file, 'r') as f:
                self.ignore_list = set(f.read().splitlines())
        else:
            self.ignore_list = set()

    def create_repo(self):
        """Initialize the repository in a directory."""
        if not os.path.exists(self.repo_dir):
            os.makedirs(self.repo_dir)
            with open(self.history_file, 'w') as f:
                json.dump([], f)
            with open(self.stage_file, 'w') as f:
                json.dump([], f)
            with open(self.branch_file, 'w') as f:
                json.dump({"main": []}, f)
            open(self.ignore_file, 'w').close()  # Create an empty .vcsignore
        else:
            raise Exception("Repository already exists!")

    def add(self, file_name):
        """Stage a file, provided the file exists and isn't ignored."""
        if file_name in self.ignore_list:
            raise Exception(f"File '{file_name}' is ignored and cannot be added.")
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"File '{file_name}' not found.")
        with open(self.stage_file, 'r+') as f:
            staged = json.load(f)
            if file_name not in staged:
                staged.append(file_name)
            f.seek(0)
            json.dump(staged, f, indent=4)

    def commit(self, message):
        """Commit the staged files with a message."""
        with open(self.stage_file, 'r') as f:
            staged = json.load(f)

        if not staged:
            raise Exception("No files staged for commit.")

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

        # Clear staged files after commit
        with open(self.stage_file, 'w') as f:
            json.dump([], f)

    def create_branch(self, branch_name):
        """Create a new branch."""
        with open(self.branch_file, 'r+') as f:
            branches = json.load(f)
            if branch_name in branches:
                raise Exception(f"Branch '{branch_name}' already exists.")
            branches[branch_name] = []
            f.seek(0)
            json.dump(branches, f, indent=4)

    def view_commit_history(self):
        """Return the commit history."""
        with open(self.history_file, 'r') as f:
            return json.load(f)

    def clone(self, new_name):
        """Clone the repository to a new directory."""
        if os.path.exists(new_name):
            raise Exception(f"Target directory '{new_name}' already exists!")
        copytree(self.name, new_name)

    def merge(self, branch_name):
        """Merge a branch into the current branch (no conflict resolution)."""
        with open(self.branch_file, 'r+') as f:
            branches = json.load(f)
            if branch_name not in branches:
                raise Exception(f"Branch '{branch_name}' does not exist.")
            current_branch = "main"  # assuming "main" as the current branch
            current_files = branches[current_branch]
            branch_files = branches[branch_name]

            # Detect conflicts (files that exist in both branches with different contents)
            conflicts = set(current_files) & set(branch_files)
            if conflicts:
                raise Exception(f"Conflicting files found: {', '.join(conflicts)}")
            
            # Merge files (this is simplified without actual file merging logic)
            branches[current_branch] += branch_files
            f.seek(0)
            json.dump(branches, f, indent=4)

    def diff(self, branch_name):
        """Show a diff between the current branch and another branch."""
        with open(self.branch_file, 'r') as f:
            branches = json.load(f)
            if branch_name not in branches:
                raise Exception(f"Branch '{branch_name}' does not exist.")
            current_branch = "main"  # assuming "main" as the current branch
            current_files = branches[current_branch]
            branch_files = branches[branch_name]

            # Get files in both branches
            added_files = set(branch_files) - set(current_files)
            removed_files = set(current_files) - set(branch_files)

            diff_output = []
            if added_files:
                diff_output.append(f"Files added in {branch_name}: {', '.join(added_files)}")
            if removed_files:
                diff_output.append(f"Files removed in {branch_name}: {', '.join(removed_files)}")

            return "\n".join(diff_output) if diff_output else "No differences."

    def ignore(self, file_name):
        """Add a file to the ignore list."""
        if file_name not in self.ignore_list:
            self.ignore_list.add(file_name)
            with open(self.ignore_file, 'a') as f:
                f.write(f"{file_name}\n")

    def view_ignore_list(self):
        """Return the list of ignored files."""
        return self.ignore_list
