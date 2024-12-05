# Source Control System

## Description
This project is a custom version control system that provides functionalities similar to Git. It is a lightweight alternative for tracking changes, managing branches, and maintaining a repository's history. The system allows users to initialize repositories, commit changes, create and manage branches, merge them, and view diffs between commits. Additionally, it supports ignoring files and provides both an interactive shell and non-interactive command-line mode for user convenience. This will be packaged and run as an .exe file in from the dist folder

For this repo, I have pushed all the repos I created using this code for confirmation, in order to follow the steps provided, remove these folders: clone,my_repo, repo. The .exe file will be overwritten.

## Features that are intergrated

1. **Repository Initialization**:
   - Create a new repository using the `init` command.
   
2. **File Staging and Committing**:
   - Stage files using the `add` command.
   - Commit changes with the `commit` command.
   
3. **Branch Management**:
   - Create branches with the `branch` command.
   - Switch between branches using `switch_branch`.
   
4. **Logging**:
   - View the history of commits using the `log` command.

5. **Merging**:
   - Merge branches and resolve conflicts with the `merge` command.
   
6. **Diff Viewing**:
   - Compare changes using the `diff` command.

7. **Ignoring Files**:
   - Specify files or directories to exclude from tracking using the `ignore` command.
   
8. **Interactive CLI**:
   - Use an intuitive interactive mode to execute commands step-by-step. this provides user with directions on how to add commands
   
9. **Non-Interactive Mode**:
   - Run commands directly from the terminal for scripting purposes.


## Project Set-Up and Run documentation 

### Setup Python Environment

I am using both cmd for windows to run python commands and for vscode, i have set up windows subsystem for linux for pushing to this repo.

Install Python for windows (if not already installed):

Make sure to check the option to add Python to your PATH during installation.
Set up a virtual environment (recommended):

In the terminal or command prompt, navigate to your project directory.

Run the following command to create a virtual environment:

```bash
python -m venv venv
```
Activate the virtual environment:
On Windows:

```bash
venv\Scripts\activate
```
On Linux:
```bash
source venv/bin/activate
```
### Install dependencies:

Create a requirements.txt file to list your dependencies. 

```plaintext
colorama
```
Install the dependencies:

```bash
pip install -r requirements.txt
```
Create setup.py for packaging the project:

```python
from setuptools import setup, find_packages

setup(
    name='source_control_system',
    version='0.1',
    packages=find_packages(),
    install_requires=['colorama'],
    entry_points={
        'console_scripts': [
            'vcs=src.vcs:main',  # Adds a command-line script for vcs.py
        ],
    },
)

```
### project structure

```plaintext

source_control_system/
│
├── src/
│   ├── __init__.py
│   ├── vcs.py              # CLI Entry point
│   ├── repo.py             # Repository logic
│   ├── utils.py            # Utilities (animations, progress indicators)
│  
├── tests/
│   ├── __init__.py      
│   ├── test_vcs.py         # Tests for CLI commands
├── .gitignore
├── requirements.txt
├── README.md
├── setup.py
└── build/                  # Build files for converting to .exe
```
### Code Implementation

Create vcs.py file. this file will import logic for the system from repo.py. This will be able to implement the  both interactive and non interactive terminal.

src/vcs.py (Main Logic for Version Control System)

```python
import sys
import os
import argparse

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import sys
import os
import argparse
from src.repo import Repository
from src.utils import display_progress, display_message
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def get_input(prompt, default=None):
    """Function to ask for user input with a default."""
    user_input = input(f"{prompt} [{default}]: ").strip()
    return user_input or default

def execute_command_in_shell(command):
    """Function to handle shell-like commands such as file creation or navigation."""
    if command.startswith("touch "):  # Create a new file
        file_name = command.split(" ", 1)[1]
        with open(file_name, 'w') as f:
            f.write("")
        print(Fore.GREEN + f"File '{file_name}' created.")
    elif command.startswith("cd "):  # Change directory
        dir_path = command.split(" ", 1)[1]
        try:
            os.chdir(dir_path)
            print(Fore.GREEN + f"Changed directory to {os.getcwd()}")
        except FileNotFoundError:
            print(Fore.RED + f"Directory '{dir_path}' not found.")
    elif command == "pwd":  # Print working directory
        print(Fore.GREEN + f"Current directory: {os.getcwd()}")
    elif command == "ls":  # List files in current directory
        files = os.listdir(os.getcwd())
        print(Fore.GREEN + "\n".join(files))
    elif command.startswith("rm "):  # Remove file
        file_name = command.split(" ", 1)[1]
        try:
            os.remove(file_name)
            print(Fore.GREEN + f"File '{file_name}' removed.")
        except FileNotFoundError:
            print(Fore.RED + f"File '{file_name}' not found.")
    else:
        print(Fore.RED + "Invalid shell command.")

def main():
    print(Fore.CYAN + "Welcome to the Python-based Distributed Version Control System\n")
    
    parser = argparse.ArgumentParser(description="Python-based Distributed Version Control System")
    subparsers = parser.add_subparsers(dest="command")

    # Initialize a repository
    parser_init = subparsers.add_parser("init")
    parser_init.add_argument("repo_name", help="Name of the repository to initialize", nargs='?')

    # Add a file to staging
    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("repo_name", help="Repository name")
    parser_add.add_argument("file_name", help="File to add to staging")

    # Commit changes
    parser_commit = subparsers.add_parser("commit")
    parser_commit.add_argument("repo_name", help="Repository name")
    parser_commit.add_argument("message", help="Commit message")

    # Create a branch
    parser_branch = subparsers.add_parser("branch")
    parser_branch.add_argument("repo_name", help="Repository name")
    parser_branch.add_argument("branch_name", help="Branch to create")

    # Switch branches
    parser_switch = subparsers.add_parser("switch_branch")
    parser_switch.add_argument("repo_name", help="Repository name")
    parser_switch.add_argument("branch_name", help="Branch to switch to")

    # Clone a repository
    parser_clone = subparsers.add_parser("clone")
    parser_clone.add_argument("repo_name", help="Repository name to clone")
    parser_clone.add_argument("new_name", help="Name of the cloned repository")

    # View commit history
    parser_log = subparsers.add_parser("log")
    parser_log.add_argument("repo_name", help="Repository name")

    # Merge branches
    parser_merge = subparsers.add_parser("merge")
    parser_merge.add_argument("repo_name", help="Repository name")
    parser_merge.add_argument("branch_name", help="Branch to merge into current branch")

    # View differences between branches
    parser_diff = subparsers.add_parser("diff")
    parser_diff.add_argument("repo_name", help="Repository name")
    parser_diff.add_argument("branch_name", help="Branch to compare against the current branch")

    # Ignore files
    parser_ignore = subparsers.add_parser("ignore")
    parser_ignore.add_argument("repo_name", help="Repository name")
    parser_ignore.add_argument("file_name", help="File to add to the ignore list")

    # View ignored files
    parser_view_ignore = subparsers.add_parser("view_ignore_list")
    parser_view_ignore.add_argument("repo_name", help="Repository name")

    args = parser.parse_args()

    # Default to interactive if no command was passed
    if not args.command:
        print(Fore.YELLOW + "No command passed. Switching to interactive mode.")
        while True:
            try:
                print(Fore.MAGENTA + f"Current directory: {os.getcwd()}")
                print(Fore.MAGENTA + "Choose an action: init, add, commit, branch, switch_branch, clone, log, merge, diff, ignore, view_ignore_list, shell (to enter shell mode), or exit")
                command = input(Fore.GREEN + "Command: ").strip().lower()

                if command == "init":
                    repo_name = get_input("Enter repository name", "my_repo")
                    repo = Repository(repo_name)
                    repo.create_repo()
                    print(Fore.GREEN + f"Repository '{repo_name}' initialized.")
                elif command == "add":
                    repo_name = get_input("Enter repository name")
                    file_name = get_input("Enter file name")
                    repo = Repository(repo_name)
                    repo.add(file_name)
                    print(Fore.GREEN + f"File '{file_name}' staged.")
                elif command == "commit":
                    repo_name = get_input("Enter repository name")
                    message = get_input("Enter commit message")
                    repo = Repository(repo_name)
                    repo.commit(message)
                    display_progress("Committing changes", steps=3)
                    print(Fore.GREEN + f"Commit added: {message}")
                elif command == "branch":
                    repo_name = get_input("Enter repository name")
                    branch_name = get_input("Enter branch name")
                    repo = Repository(repo_name)
                    repo.create_branch(branch_name)
                    print(Fore.GREEN + f"Branch '{branch_name}' created.")
                elif command == "switch_branch":
                    repo_name = get_input("Enter repository name")
                    branch_name = get_input("Enter branch name")
                    repo = Repository(repo_name)
                    repo.switch_branch(branch_name)
                    print(Fore.GREEN + f"Switched to branch '{branch_name}'.")
                elif command == "clone":
                    repo_name = get_input("Enter repository name")
                    new_name = get_input("Enter new repository name")
                    repo = Repository(repo_name)
                    repo.clone(new_name)
                    display_progress("Cloning repository", steps=5)
                    print(Fore.GREEN + f"Repository '{repo_name}' cloned as '{new_name}'.")
                elif command == "log":
                    repo_name = get_input("Enter repository name")
                    repo = Repository(repo_name)
                    history = repo.view_commit_history()
                    print(Fore.CYAN + "Commit History:")
                    for commit in history:
                        print(Fore.YELLOW + f" - {commit['date']}: {commit['message']}")
                elif command == "merge":
                    repo_name = get_input("Enter repository name")
                    branch_name = get_input("Enter branch to merge")
                    repo = Repository(repo_name)
                    try:
                        repo.merge(branch_name)
                        print(Fore.GREEN + f"Branch '{branch_name}' merged successfully.")
                    except Exception as e:
                        print(Fore.RED + str(e))
                elif command == "diff":
                    repo_name = get_input("Enter repository name")
                    branch_name = get_input("Enter branch to compare")
                    repo = Repository(repo_name)
                    diff = repo.diff(branch_name)
                    print(Fore.CYAN + "Differences:")
                    print(Fore.YELLOW + diff)
                elif command == "ignore":
                    repo_name = get_input("Enter repository name")
                    file_name = get_input("Enter file to ignore")
                    repo = Repository(repo_name)
                    repo.ignore(file_name)
                    print(Fore.GREEN + f"File '{file_name}' added to the ignore list.")
                elif command == "view_ignore_list":
                    repo_name = get_input("Enter repository name")
                    repo = Repository(repo_name)
                    ignored_files = repo.view_ignore_list()
                    print(Fore.CYAN + "Ignored Files:")
                    for file in ignored_files:
                        print(Fore.YELLOW + f" - {file}")
                elif command == "shell":
                    print(Fore.YELLOW + "Entering shell mode. You can now use commands like 'touch', 'cd', 'ls', 'rm'. Type 'exit' to leave shell mode.")
                    while True:
                        shell_command = input(Fore.GREEN + "Shell Command: ").strip().lower()
                        if shell_command == "exit":
                            break
                        try:
                            execute_command_in_shell(shell_command)
                        except Exception as shell_error:
                            print(Fore.RED + f"Shell Error: {shell_error}")
                elif command == "exit":
                    print(Fore.RED + "Exiting program.")
                    break
                else:
                    print(Fore.RED + "Invalid command, please try again.")
            except Exception as main_error:
                print(Fore.RED + f"Error: {main_error}")
        return

    # Execute commands based on parsed arguments
    repo = Repository(args.repo_name)
    try:
        if args.command == "init":
            repo.create_repo()
            print(Fore.GREEN + f"Repository '{args.repo_name}' initialized.")
        elif args.command == "add":
            repo.add(args.file_name)
            print(Fore.GREEN + f"File '{args.file_name}' staged.")
        elif args.command == "commit":
            repo.commit(args.message)
            display_progress("Committing changes", steps=3)
            print(Fore.GREEN + f"Commit added: {args.message}")
        elif args.command == "branch":
            repo.create_branch(args.branch_name)
            print(Fore.GREEN + f"Branch '{args.branch_name}' created.")
        elif args.command == "switch_branch":
            repo.switch_branch(args.branch_name)
            print(Fore.GREEN + f"Switched to branch '{args.branch_name}'.")
        elif args.command == "clone":
            repo.clone(args.new_name)
            display_progress("Cloning repository", steps=5)
            print(Fore.GREEN + f"Repository '{args.repo_name}' cloned as '{args.new_name}'.")
        elif args.command == "log":
            history = repo.view_commit_history()
            print(Fore.CYAN + "Commit History:")
            for commit in history:
                print(Fore.YELLOW + f" - {commit['date']}: {commit['message']}")
        elif args.command == "merge":
            repo.merge(args.branch_name)
            print(Fore.GREEN + f"Branch '{args.branch_name}' merged successfully.")
        elif args.command == "diff":
            diff = repo.diff(args.branch_name)
            print(Fore.CYAN + "Differences:")
            print(Fore.YELLOW + diff)
        elif args.command == "ignore":
            repo.ignore(args.file_name)
            print(Fore.GREEN + f"File '{args.file_name}' added to the ignore list.")
        elif args.command == "view_ignore_list":
            ignored_files = repo.view_ignore_list()
            print(Fore.CYAN + "Ignored Files:")
            for file in ignored_files:
                print(Fore.YELLOW + f" - {file}")
        else:
            parser.print_help()
    except Exception as e:
        print(Fore.RED + str(e))

if __name__ == "__main__":
    main()

```
src/repo.py (Repository Handling)
This code implements the repo.py functions

```python

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

```

src/utils.py (User Interface - Colorful )
```python
import time
from colorama import Fore, Style

def display_progress(task, steps=3):
    print(Fore.YELLOW + f"{task}...")
    for _ in range(steps):
        print(Fore.YELLOW + ".", end='', flush=True)
        time.sleep(0.5)
    print(Fore.GREEN + " Done!")

def display_message(message):
    print(Fore.CYAN + message)

```
### How to Run the Program

These are the functions we will be testing:

init, add, commit, branch, switch_branch, clone, log, merge, diff, ignore, view_ignore_list, shell, or exit


| Command            | Description                                       |
|--------------------|---------------------------------------------------|
| `init`             | Initialize a new repository.                      |
| `add <file>`       | Stage a file for the next commit.                 |
| `commit`        | Commit staged files with a message.               |
| `branch`           | Create a new branch.                              |
| `switch_branch`    | Switch to an existing branch.                     |
| `log`              | View commit history.                              |
| `merge`            | Merge one branch into another.                    |
| `diff`             | View differences between commits or branches.     |
| `ignore`           | Specify files to exclude from tracking.           |
| `view_ignore_list` | View the list of ignored files.                   |
| `exit`             | Exit the interactive mode.                        |

#### End to End work-flow

We will test the test_vcs.py and then do end to end workflow in both non interactive and user - friendly interactive mode
Non interactive mode:
Open cmd from the project folder

```bash
python python -m unittest tests/test_vcs.py
python src/vcs.py init my_repo
echo "Initial content" > my_repo/file1.txt
python src/vcs.py add my_repo file1.txt
python src/vcs.py commit my_repo "Initial commit"
python src/vcs.py branch my_repo feature_branch
python src/vcs.py switch_branch my_repo feature_branch
echo "Hello Feature Branch" > my_repo/feature.txt
python src/vcs.py add my_repo feature.txt
python src/vcs.py commit my_repo " commit"
python src/vcs.py diff my_repo main
python src/vcs.py ignore my_repo feature.txt
python src/vcs.py view_ignore_list my_repo
python src/vcs.py merge my_repo main
python src/vcs.py log  my_repo
python src/vcs.py clone  my_repo clone
```

using the above format for usage here is the output


![Command Output](images/vcs-logo.png) 
![Command Output](images/vcs-logo.png) 

- step one is running the test file
- step two is initializing a repo within the folder, you cannot init the same repo twice
- step three is creating a file
- step four is adding file, it can only be added if it is within the repo
- step five is commiting the changes 
- step six is creating new branch which copies all the commits 
- step seven is switching from main to new branch 
- step eight is creating new file
- step nine adding new file to new branch
- step ten is commiting in new branch
- step 11 is checking what is different, the output shows main has one less file which system sees as removed
- step 12 is adding file to ignore list
- step 13 is checking ignore list
- step 14 is merging, then repo log then cloning


Interactive mode commands usage. These commands ensure user interactivity. The shell command is used to navigate to repo , to add a file and to move back to the main folder. These shell commands are linux based commands as I chose linux because it is used by most developers:

```bash
python src/vcs.py
Command: init
Enter repository name [my_repo]: repo
Command: shell
Shell Command: cd repo
Shell Command: touch test.txt
Shell Command: cd ..
Shell Command: exit
Command: add
Enter repository name [None]: repo
Enter file name [None]: test.txt
Command: commit
Enter repository name [None]: repo
Enter commit message [None]: first
Command: branch
Enter repository name [None]: repo
Enter branch name [None]: new
Branch 'new' created.
Command: switch_branch
Enter repository name [None]: repo
Enter branch name [None]: new
Command: diff
Enter repository name [None]: repo
Enter branch to compare [None]: main
Command: ignore
Enter repository name [None]: repo
Enter file to ignore [None]: test.txt
view_ignore_list, shell (to enter shell mode), or exit
Command: view_ignore_list
Enter repository name [None]: repo
Command: exit
Exiting program.

```


![Command Output](images/vcs-logo.png) 
![Command Output](images/vcs-logo.png) 

#### Packaging the repo and runnig the .exe 

```bash
pip install pyinstaller
pyinstaller --onefile src/vcs.py
```
The folder will be built inside the dist folder,here is the video of how i ran the .exe file afterwards.

[![Demo Video](<thumbnail-image-path>)](<video-url>)  
