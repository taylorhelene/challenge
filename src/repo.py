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
        self.active_branch_file = os.path.join(self.repo_dir, "active_branch.txt")
        self.ignore_file = os.path.join(self.repo_dir, ".vcsignore")
        self._load_ignore_list()

    def _load_ignore_list(self):
        """Load files that should be ignored from .vcsignore."""
        if os.path.exists(self.ignore_file):
            with open(self.ignore_file, 'r') as f:
                self.ignore_list = set(f.read().splitlines())
        else:
            self.ignore_list = set()

    def _get_active_branch(self):
        """Retrieve the currently active branch."""
        if os.path.exists(self.active_branch_file):
            with open(self.active_branch_file, 'r') as f:
                return f.read().strip()
        return "main"

    def _set_active_branch(self, branch_name):
        """Set the active branch."""
        with open(self.active_branch_file, 'w') as f:
            f.write(branch_name)

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
            open(self.active_branch_file, 'w').write("main")
            open(self.ignore_file, 'w').close()  # Create an empty .vcsignore
        else:
            raise Exception("Repository already exists!")

    def add(self, file_name):
        """Stage a file for commit."""
        file_path = os.path.join(self.name, file_name)
        if not os.path.exists(file_path):
            raise Exception(f"File '{file_name}' not found in repository directory.")
        
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

        current_branch = self._get_active_branch()
        with open(self.branch_file, 'r+') as f:
            branches = json.load(f)
            if current_branch not in branches:
                branches[current_branch] = []

            for file_name in staged:
                file_path = os.path.join(self.name, file_name)
                with open(file_path, 'r') as file:
                    content = file.read()
                branches[current_branch].append({"file": file_name, "content": content})

            f.seek(0)
            json.dump(branches, f, indent=4)

        with open(self.stage_file, 'w') as f:
            json.dump([], f)

    def create_branch(self, branch_name):
        """Create a new branch."""
        with open(self.branch_file, 'r+') as f:
            branches = json.load(f)
            if branch_name in branches:
                raise Exception(f"Branch '{branch_name}' already exists.")
            
            current_branch = self._get_active_branch()
            if current_branch not in branches:
                raise Exception(f"Current branch '{current_branch}' not found.")

            branches[branch_name] = branches[current_branch].copy()
            f.seek(0)
            json.dump(branches, f, indent=4)

    def switch_branch(self, branch_name):
        """Switch to a different branch."""
        with open(self.branch_file, 'r') as f:
            branches = json.load(f)
            if branch_name not in branches:
                raise Exception(f"Branch '{branch_name}' does not exist.")
        
        self._set_active_branch(branch_name)

    def diff(self, branch_name):
        """Show a diff between the current branch and another branch."""
        with open(self.branch_file, 'r') as f:
            branches = json.load(f)

        if branch_name not in branches:
            raise Exception(f"Branch '{branch_name}' does not exist.")
        
        current_branch = self._get_active_branch()
        current_files = {file["file"]: file["content"] for file in branches[current_branch]}
        branch_files = {file["file"]: file["content"] for file in branches[branch_name]}

        added_files = set(branch_files) - set(current_files)
        removed_files = set(current_files) - set(branch_files)
        common_files = set(current_files) & set(branch_files)

        diff_output = []
        if added_files:
            diff_output.append(f"Files added in {branch_name}: {', '.join(added_files)}")
        if removed_files:
            diff_output.append(f"Files removed in {branch_name}: {', '.join(removed_files)}")
        for file in common_files:
            if current_files[file] != branch_files[file]:
                diff = "\n".join(unified_diff(
                    current_files[file].splitlines(),
                    branch_files[file].splitlines(),
                    fromfile=f"{file} ({current_branch})",
                    tofile=f"{file} ({branch_name})",
                    lineterm=''
                ))
                diff_output.append(f"Changes in {file}:\n{diff}")
        
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

    def view_commit_history(self):
        """View commit history."""
        with open(self.history_file, 'r') as f:
            return json.load(f)

    def clone(self, new_name):
        """Clone the repository."""
        if os.path.exists(new_name):
            raise Exception(f"Directory '{new_name}' already exists.")
        copytree(self.name, new_name)

    def merge(self, branch_name):
        """Merge a branch into the current branch."""
        with open(self.branch_file, 'r+') as f:
            branches = json.load(f)

            if branch_name not in branches:
                raise Exception(f"Branch '{branch_name}' does not exist.")
            
            current_branch = self._get_active_branch()
            if current_branch not in branches:
                raise Exception(f"Current branch '{current_branch}' not found.")
            
            branches[current_branch].extend(branches[branch_name])
            f.seek(0)
            json.dump(branches, f, indent=4)

    def create_file(repo_name, file_name, content):
        """Creates a file in the repository with the given content."""
        file_path = os.path.join(repo_name, file_name)
        with open(file_path, "w") as f:
            f.write(content)
        print(f"File '{file_name}' created in repository '{repo_name}'.")
