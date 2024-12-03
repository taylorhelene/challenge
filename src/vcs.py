import sys
import os
import argparse

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
from colorama import Fore, Style, init

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.repo import Repository
from src.utils import display_progress, display_message

# Initialize colorama
init(autoreset=True)

def get_input(prompt, default=None):
    """Function to ask for user input with a default."""
    user_input = input(f"{prompt} [{default}]: ").strip()
    return user_input or default

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

    # Clone a repository
    parser_clone = subparsers.add_parser("clone")
    parser_clone.add_argument("repo_name", help="Repository name to clone")
    parser_clone.add_argument("new_name", help="Name of the cloned repository")

    # View commit history
    parser_log = subparsers.add_parser("log")
    parser_log.add_argument("repo_name", help="Repository name")

    args = parser.parse_args()

    # Default to interactive if no command was passed
    if not args.command:
        print(Fore.YELLOW + "No command passed. Switching to interactive mode.")
        while True:
            print(Fore.MAGENTA + "Choose an action: init, add, commit, branch, clone, log, or exit")
            command = input(Fore.GREEN + "Command: ").strip().lower()

            if command == "init":
                repo_name = get_input("Enter repository name", "my_repo")
                repo = Repository(repo_name)
                repo.create_repo()
                print(Fore.GREEN + f"Repository '{repo_name}' initialized.")
            elif command == "add":
                repo_name = get_input("Enter repository name")
                file_name = get_input("Enter file name")
                try:
                    repo = Repository(repo_name)
                    repo.add(file_name)
                    print(Fore.GREEN + f"File '{file_name}' staged.")
                except Exception as e:
                    print(Fore.RED + str(e))
            elif command == "commit":
                repo_name = get_input("Enter repository name")
                message = get_input("Enter commit message")
                try:
                    repo = Repository(repo_name)
                    repo.commit(message)
                    display_progress("Committing changes", steps=3)
                    print(Fore.GREEN + f"Commit added: {message}")
                except Exception as e:
                    print(Fore.RED + str(e))
            elif command == "branch":
                repo_name = get_input("Enter repository name")
                branch_name = get_input("Enter branch name")
                try:
                    repo = Repository(repo_name)
                    repo.create_branch(branch_name)
                    print(Fore.GREEN + f"Branch '{branch_name}' created.")
                except Exception as e:
                    print(Fore.RED + str(e))
            elif command == "clone":
                repo_name = get_input("Enter repository name")
                new_name = get_input("Enter new repository name")
                try:
                    repo = Repository(repo_name)
                    repo.clone(new_name)
                    display_progress("Cloning repository", steps=5)
                    print(Fore.GREEN + f"Repository '{repo_name}' cloned as '{new_name}'.")
                except Exception as e:
                    print(Fore.RED + str(e))
            elif command == "log":
                repo_name = get_input("Enter repository name")
                try:
                    repo = Repository(repo_name)
                    history = repo.view_commit_history()
                    print(Fore.CYAN + "Commit History:")
                    for commit in history:
                        print(Fore.YELLOW + f" - {commit['date']}: {commit['message']}")
                except Exception as e:
                    print(Fore.RED + str(e))
            elif command == "exit":
                print(Fore.RED + "Exiting program.")
                break
            else:
                print(Fore.RED + "Invalid command, please try again.")
        return

    # Map commands to repository actions
    try:
        if args.command == "init":
            repo_name = args.repo_name or get_input("Enter repository name", "my_repo")
            repo = Repository(repo_name)
            repo.create_repo()
            print(Fore.GREEN + f"Repository '{repo_name}' initialized.")
        elif args.command == "add":
            repo = Repository(args.repo_name)
            repo.add(args.file_name)
            print(Fore.GREEN + f"File '{args.file_name}' staged.")
        elif args.command == "commit":
            repo = Repository(args.repo_name)
            repo.commit(args.message)
            display_progress("Committing changes", steps=3)
            print(Fore.GREEN + f"Commit added: {args.message}")
        elif args.command == "branch":
            repo = Repository(args.repo_name)
            repo.create_branch(args.branch_name)
            print(Fore.GREEN + f"Branch '{args.branch_name}' created.")
        elif args.command == "clone":
            repo = Repository(args.repo_name)
            repo.clone(args.new_name)
            display_progress("Cloning repository", steps=5)
            print(Fore.GREEN + f"Repository '{args.repo_name}' cloned as '{args.new_name}'.")
        elif args.command == "log":
            repo = Repository(args.repo_name)
            history = repo.view_commit_history()
            print(Fore.CYAN + "Commit History:")
            for commit in history:
                print(Fore.YELLOW + f" - {commit['date']}: {commit['message']}")
        else:
            parser.print_help()
    except Exception as e:
        print(Fore.RED + str(e))

if __name__ == "__main__":
    main()
