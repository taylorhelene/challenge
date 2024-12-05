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
