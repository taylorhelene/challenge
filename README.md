# Source Control System


## Setup Python Environment

Install Python (if not already installed):

Visit python.org/downloads and install the latest version of Python.
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
## Install dependencies:

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
## Code Implementation

src/vcs.py (Main Logic for Version Control System)

```python
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
```
src/repo.py (Repository Handling)
```python
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
```
src/ui.py (User Interface - Colorful and Animations)
```python
from colorama import init, Fore, Style
import time

init(autoreset=True)

def display_welcome_message():
    print(Fore.GREEN + Style.BRIGHT + "Welcome to the Python-based Source Control System!")
    print(Fore.CYAN + "This system allows you to initialize repos, stage files, commit changes, create branches, and more.")

def show_error(message):
    print(Fore.RED + f"ERROR: {message}")

def show_success(message):
    print(Fore.GREEN + f"SUCCESS: {message}")

def simulate_loading():
    for _ in range(3):
        print(Fore.YELLOW + ".", end='', flush=True)
        time.sleep(0.5)
    print()
```
4. How to Run the Program
To run the program, simply follow these steps:

Install Dependencies: If you haven’t already, install the necessary dependencies using:

bash
Copy code
pip install -r requirements.txt
Run the Program: In the terminal, you can run the program as a script or by using the vcs command if you configured setup.py for easy CLI execution:

bash
Copy code
python src/vcs.py
Alternatively, you can run it as:
(I ran mine this way because it produces no error ): 
set PYTHONPATH=C:\Users\user\Desktop\Utest2\challenge && python src\vcs.py

Run your code this way and replace the path with your path to folder

bash
Copy code
set PYTHONPATH=C:\Users\user\folder && python src\vcs.py

Testing: To write tests, you can use pytest for the repository and UI tests. Example test for repo.py:

python
Copy code
def test_commit_history():
    repo = Repository('test_repo')
    repo.create_repo()
    repo.commit('Initial commit')
    history = repo.view_commit_history()
    assert len(history) == 1
    assert history[0]['message'] == 'Initial commit'
Generate Documentation: You can use Sphinx to generate detailed documentation for the project, covering the logic, code structure, and any unique features.



C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py create_branch my_repo feature_branch
Welcome to the Python-based Distributed Version Control System

Branch 'feature_branch' created.

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py switch_branch my_repo feature_branch
Welcome to the Python-based Distributed Version Control System

Switched to branch 'feature_branch'.

C:\Users\user\Desktop\Utest2\challenge>echo "Hello Feature" > my_repo/feature.txt

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py add my_repo feature.txt
Welcome to the Python-based Distributed Version Control System

File 'feature.txt' staged.

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py commit my_repo "Add feature.txt"
Welcome to the Python-based Distributed Version Control System

Committing changes...
... Done!
Commit added: Add feature.txt

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py log my_repo
Welcome to the Python-based Distributed Version Control System

usage: vcs.py [-h] {init,add,commit,create_branch,switch_branch,diff} ...
vcs.py: error: argument command: invalid choice: 'log' (choose from 'init', 'add', 'commit', 'create_branch', 'switch_branch', 'diff')

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py log my_repo
Traceback (most recent call last):
  File "C:\Users\user\Desktop\Utest2\challenge\src\vcs.py", line 4, in <module>
    from src.repo import Repository
ModuleNotFoundError: No module named 'src'

C:\Users\user\Desktop\Utest2\challenge>python -m unittest tests/test_vcs.py
C:\Users\user\Desktop\Utest2\challenge\src\repo.py:48: ResourceWarning: unclosed file <_io.TextIOWrapper name='test_repo\\.vcs\\active_branch.txt' mode='w' encoding='cp1252'>
  open(self.active_branch_file, 'w').write("main")
ResourceWarning: Enable tracemalloc to get the object allocation traceback
....
----------------------------------------------------------------------
Ran 4 tests in 0.309s

OK

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py init my_repo
Traceback (most recent call last):
  File "C:\Users\user\Desktop\Utest2\challenge\src\vcs.py", line 4, in <module>
    from src.repo import Repository
ModuleNotFoundError: No module named 'src'

C:\Users\user\Desktop\Utest2\challenge>python -m unittest tests/test_vcs.py
C:\Users\user\Desktop\Utest2\challenge\src\repo.py:48: ResourceWarning: unclosed file <_io.TextIOWrapper name='test_repo\\.vcs\\active_branch.txt' mode='w' encoding='cp1252'>
  open(self.active_branch_file, 'w').write("main")
ResourceWarning: Enable tracemalloc to get the object allocation traceback
....
----------------------------------------------------------------------
Ran 4 tests in 0.110s

OK

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py init my_repo
Welcome to the Python-based Distributed Version Control System

Repository 'my_repo' initialized.

C:\Users\user\Desktop\Utest2\challenge>echo "Initial content" > my_repo/file1.txt

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py add my_repo/file1.txt
Welcome to the Python-based Distributed Version Control System

usage: vcs.py add [-h] repo_name file_name
vcs.py add: error: the following arguments are required: file_name

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py add my_repo/file1.txt
Welcome to the Python-based Distributed Version Control System

usage: vcs.py add [-h] repo_name file_name
vcs.py add: error: the following arguments are required: file_name

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py add my_repo file1.txt
Welcome to the Python-based Distributed Version Control System

File 'file1.txt' staged.

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py commit "Add file2.txt to feature branch"
Welcome to the Python-based Distributed Version Control System

usage: vcs.py commit [-h] repo_name message
vcs.py commit: error: the following arguments are required: message

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py commit my_repo "Initial commit"
Welcome to the Python-based Distributed Version Control System

Committing changes...
... Done!
Commit added: Initial commit

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py create_branch my_repo feature_branch
Welcome to the Python-based Distributed Version Control System

usage: vcs.py [-h] {init,add,commit,branch,switch_branch,clone,log,merge,diff,ignore,view_ignore_list} ...
vcs.py: error: argument command: invalid choice: 'create_branch' (choose from 'init', 'add', 'commit', 'branch', 'switch_branch', 'clone', 'log', 'merge', 'diff', 'ignore', 'view_ignore_list')

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py branch my_repo feature_branch
Welcome to the Python-based Distributed Version Control System

Branch 'feature_branch' created.

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py switch_branch my_repo feature_branch
Welcome to the Python-based Distributed Version Control System

Switched to branch 'feature_branch'.

C:\Users\user\Desktop\Utest2\challenge>echo "Hello Feature Branch" > my_repo/featue.txt

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py add my_repo feature.txt
Welcome to the Python-based Distributed Version Control System

File 'feature.txt' not found in repository directory.

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py add my_repo featue.txt
Welcome to the Python-based Distributed Version Control System

File 'featue.txt' staged.

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py commit my_repo " commit"
Welcome to the Python-based Distributed Version Control System

Committing changes...
... Done!
Commit added:  commit

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py diff my_repo main
Welcome to the Python-based Distributed Version Control System

Differences:
Files removed in main: featue.txt

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py merge feature_branch
Welcome to the Python-based Distributed Version Control System

usage: vcs.py merge [-h] repo_name branch_name
vcs.py merge: error: the following arguments are required: branch_name

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py my_repo merge main feature_branch
Welcome to the Python-based Distributed Version Control System

usage: vcs.py [-h] {init,add,commit,branch,switch_branch,clone,log,merge,diff,ignore,view_ignore_list} ...
vcs.py: error: argument command: invalid choice: 'my_repo' (choose from 'init', 'add', 'commit', 'branch', 'switch_branch', 'clone', 'log', 'merge', 'diff', 'ignore', 'view_ignore_list')

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py  merge my_repo  main feature_branch
Welcome to the Python-based Distributed Version Control System

usage: vcs.py [-h] {init,add,commit,branch,switch_branch,clone,log,merge,diff,ignore,view_ignore_list} ...
vcs.py: error: unrecognized arguments: feature_branch

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py  merge my_repo  main
Welcome to the Python-based Distributed Version Control System

Branch 'main' merged successfully.

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py log
Welcome to the Python-based Distributed Version Control System

usage: vcs.py log [-h] repo_name
vcs.py log: error: the following arguments are required: repo_name

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py my_repo log
Welcome to the Python-based Distributed Version Control System

usage: vcs.py [-h] {init,add,commit,branch,switch_branch,clone,log,merge,diff,ignore,view_ignore_list} ...
vcs.py: error: argument command: invalid choice: 'my_repo' (choose from 'init', 'add', 'commit', 'branch', 'switch_branch', 'clone', 'log', 'merge', 'diff', 'ignore', 'view_ignore_list')

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py log  my_repo
Welcome to the Python-based Distributed Version Control System

Commit History:
 - 2024-12-04 18:18:19: Initial commit
 - 2024-12-04 18:21:17:  commit

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py ignore list
Welcome to the Python-based Distributed Version Control System

usage: vcs.py ignore [-h] repo_name file_name
vcs.py ignore: error: the following arguments are required: file_name

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py my_repo  ignore list
Welcome to the Python-based Distributed Version Control System

usage: vcs.py [-h] {init,add,commit,branch,switch_branch,clone,log,merge,diff,ignore,view_ignore_list} ...
vcs.py: error: argument command: invalid choice: 'my_repo' (choose from 'init', 'add', 'commit', 'branch', 'switch_branch', 'clone', 'log', 'merge', 'diff', 'ignore', 'view_ignore_list')

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py ignore my_repo list
Welcome to the Python-based Distributed Version Control System

File 'list' added to the ignore list.

C:\Users\user\Desktop\Utest2\challenge>python src/vcs.py clone my_repo my_repo_clone
Welcome to the Python-based Distributed Version Control System

Cloning repository...
..... Done!
Repository 'my_repo' cloned as 'my_repo_clone'.

C:\Users\user\Desktop\Utest2\challenge>



