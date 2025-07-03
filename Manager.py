import os
import sys
import math
import time
import random
import Utilities
import commands
import importlib.util

try:
    from colorama import Fore, init, Style
    init(True)
except ImportError:
    class FakeColor:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        RESET = '\033[0m'

    class FakeStyle:
        BRIGHT = '\033[1m'
        RESET_ALL = '\033[0m'

    Fore = FakeColor()
    Style = FakeStyle()

# --- Dynamic loading of addons ---
addon_commands = {}

def load_addons():
    addons_dir = os.path.join(os.path.dirname(__file__), "addons")
    if not os.path.isdir(addons_dir):
        return
    for fname in os.listdir(addons_dir):
        if fname.endswith(".txt"):
            fpath = os.path.join(addons_dir, fname)
            with open(fpath, encoding="utf-8") as f:
                content = f.read()
            if not content.startswith("#addons-manager"):
                continue
            # Search for a function def name(args):
            import re
            match = re.search(r"def\s+(\w+)\(args\):", content)
            if not match:
                continue
            func_name = match.group(1)
            # Try to execute the code to define the function
            try:
                local_env = {}
                exec(content, {}, local_env)
                if func_name in local_env and callable(local_env[func_name]):
                    addon_commands[func_name] = local_env[func_name]
            except Exception as e:
                print(Fore.RED + f"Error in addon {fname}: {e}")

load_addons()
# --- End dynamic loading of addons ---

def interface(is_loading=False):
    Utilities.clear(True)
    if is_loading:
        Utilities.charge("Loading")
    print(Fore.RED+ r"""$$\      $$\                                                             
$$$\    $$$ |                                                            
$$$$\  $$$$ | $$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  
$$\$$\$$ $$ | \____$$\ $$  __$$\  \____$$\ $$  __$$\ $$  __$$\ $$  __$$\ 
$$ \$$$  $$ | $$$$$$$ |$$ |  $$ | $$$$$$$ |$$ /  $$ |$$$$$$$$ |$$ |  \__|
$$ |\$  /$$ |$$  __$$ |$$ |  $$ |$$  __$$ |$$ |  $$ |$$   ____|$$ |      
$$ | \_/ $$ |\$$$$$$$ |$$ |  $$ |\$$$$$$$ |\$$$$$$$ |\$$$$$$$\ $$ |      
\__|     \__| \_______|\__|  \__| \_______| \____$$ | \_______|\__|      
                                           $$\   $$ |                    
                                           \$$$$$$  |                    
                                            \______/         """,Fore.BLUE+ Style.BRIGHT+ r"Made By ME")

def get_user(color=Fore.WHITE, prompt=">>"):
    inp = input(color + prompt)
    return inp

def apply_command(comm, inp):
    try:
        parts = inp.strip().split()
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]
        in_comm = any(cmd == com["name"] for com in comm) or cmd in addon_commands
        if not in_comm:
            Utilities.print_error("Unknown command")
            return

        # Commands from commands.py
        if cmd == "help":
            commands.help()
        elif cmd == "open_file":
            commands.open_file(args)
        elif cmd == "exit":
            print("Bye!")
            exit(0)
        elif cmd == "echo":
            commands.echo(args)
        elif cmd == "add":
            commands.add(args)
        elif cmd=="clear":
            interface()
        elif cmd=="show_files":
            commands.show_files(args)
        elif cmd=="goin":
            commands.goin(args)
        elif cmd=="ex":
            commands.ex(args)
        elif cmd == "mkdir":
            commands.mkdir(args)
        elif cmd == "rmdir":
            commands.rmdir(args)
        elif cmd == "rename":
            commands.rename(args)
        elif cmd == "copy":
            commands.copy(args)
        elif cmd == "move":
            commands.move(args)
        elif cmd == "cat":
            commands.cat(args)
        elif cmd == "touch":
            commands.touch(args)
        elif cmd == "whoami":
            commands.whoami(args)
        elif cmd == "date":
            commands.date(args)
        elif cmd == "reload_addons":
            commands.reload_addons(args)
        elif cmd in addon_commands:
            try:
                addon_commands[cmd](args)
            except Exception as e:
                Utilities.print_error(f"Error in addon '{cmd}': {e}")
        else:
            Utilities.print_error("Command not implemented.")
    except Exception as e:
        Utilities.print_error(str(e))

comm = commands.commands_av
interface()
while True:
    inp = get_user()
    apply_command(comm, inp)