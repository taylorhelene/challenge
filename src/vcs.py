import argparse
from src.repo import Repository
from src.utils import display_progress, display_message

def main():
    parser = argparse.ArgumentParser(description="Python-based Distributed Version Control System")
    subparsers = parser.add_subparsers(dest="command")

    # Initialize a repository
    parser_init = subparsers.add_parser("init")
    parser_init.add_argument("repo_name", help="Name of the repository to initialize")

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

    # Map commands to repository actions
    if args.command == "init":
        repo = Repository(args.repo_name)
        repo.create_repo()
        display_message(f"Repository '{args.repo_name}' initialized.")
    elif args.command == "add":
        repo = Repository(args.repo_name)
        repo.add(args.file_name)
        display_message(f"File '{args.file_name}' staged.")
    elif args.command == "commit":
        repo = Repository(args.repo_name)
        repo.commit(args.message)
        display_progress("Committing changes", steps=3)
        display_message(f"Commit added: {args.message}")
    elif args.command == "branch":
        repo = Repository(args.repo_name)
        repo.create_branch(args.branch_name)
        display_message(f"Branch '{args.branch_name}' created.")
    elif args.command == "clone":
        repo = Repository(args.repo_name)
        repo.clone(args.new_name)
        display_progress("Cloning repository", steps=5)
        display_message(f"Repository '{args.repo_name}' cloned as '{args.new_name}'.")
    elif args.command == "log":
        repo = Repository(args.repo_name)
        history = repo.view_commit_history()
        display_message("Commit History:")
        for commit in history:
            print(f" - {commit['date']}: {commit['message']}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
