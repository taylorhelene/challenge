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
