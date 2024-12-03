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
