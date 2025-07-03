import Utilities
import os
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

commands_av = [
    {"name": "open_file", "desc": "Open a file"},
    {"name": "help", "desc": "Show available commands"},
    {"name": "exit", "desc": "Exit the program"},
    {"name": "echo", "desc": "Echo the provided message"},
    {"name": "add", "desc": "Add two numbers"},
    {"name": "clear", "desc": "Clear terminal"},
    {"name": "show_files", "desc": "Show files at a directory"},
    {"name": "goin", "desc": "Navigate directories, list files with sorting, create/destroy files"},
    {"name": "ex", "desc": "Execute a command"},
    {"name": "mkdir", "desc": "Create a directory"},
    {"name": "rmdir", "desc": "Remove a directory"},
    {"name": "rename", "desc": "Rename a file or directory"},
    {"name": "copy", "desc": "Copy a file"},
    {"name": "move", "desc": "Move a file"},
    {"name": "cat", "desc": "Display file content"},
    {"name": "touch", "desc": "Create an empty file"},
    {"name": "whoami", "desc": "Show current user"},
    {"name": "date", "desc": "Show current date and time"},
    {"name": "reload_addons", "desc": "Reload all addons without restarting"}
]

def get_commands():
    return commands_av

def ex(args):
    try:
        if not args:
            Utilities.print_error("No command provided to execute.")
            return
        command = " ".join(args)
        result = os.system(command)
        if result != 0:
            Utilities.print_error(f"Command exited with code {result}")
    except Exception as e:
        Utilities.print_error(str(e))

def goin(args):
    try:
        directory = args[0] if args else "."
        if not os.path.isdir(directory):
            Utilities.print_error(f"Directory '{directory}' does not exist.")
            return
        current_dir = os.path.abspath(directory)
        print(Fore.GREEN + f"Entering goin mode in '{current_dir}'. Type 'exit_goin' to exit.")
        print(Fore.CYAN + "Type 'help' for goin commands help.")
        sort_type = "A-Z"
        while True:
            user_input = input(Fore.YELLOW + f">>goin [{current_dir}]>> " + Fore.RESET).strip()
            if not user_input:
                continue
            parts = user_input.split()
            cmd = parts[0]
            cmd_args = parts[1:]
            if cmd == "exit_goin":
                print(Fore.GREEN + "Exiting goin mode.")
                break
            elif cmd == "help":
                print(Fore.CYAN + "goin commands:")
                print(Fore.GREEN + "  rego <dir>" + Fore.WHITE + " : Change directory to <dir>")
                print(Fore.GREEN + "  ls [A-Z|Z-A|heaviest|lightest|type]" + Fore.WHITE + " : List files with optional sorting")
                print(Fore.GREEN + "  create <filename>" + Fore.WHITE + " : Create an empty file")
                print(Fore.GREEN + "  destroy <filename>" + Fore.WHITE + " : Delete a file")
                print(Fore.GREEN + "  exit_goin" + Fore.WHITE + " : Exit goin mode")
                print(Fore.GREEN + "  help" + Fore.WHITE + " : Show this help message")
                print(Fore.GREEN + "  rego before" + Fore.WHITE + " : Go to the parent directory")
            elif cmd == "rego" or cmd == "r":
                if not cmd_args:
                    Utilities.print_error("No directory specified for rego.")
                    continue
                if cmd_args[0] == "before" or cmd_args[0] == "b":
                    parent_dir = os.path.dirname(current_dir)
                    if os.path.isdir(parent_dir):
                        current_dir = parent_dir
                        print(Fore.GREEN + f"Changed directory to parent '{current_dir}'")
                    else:
                        Utilities.print_error("No parent directory found.")
                    continue
                if cmd_args and cmd_args[0].isdigit():
                    idx = int(cmd_args[0])
                    files = os.listdir(current_dir)
                    if not sort_type:
                        sort_type = 'A-Z'
                    if sort_type == "folder":
                        files = [f for f in files if os.path.isdir(os.path.join(current_dir, f))]
                        files.sort()
                    else:
                        files = sort_files(files, current_dir, sort_type)
                    if idx < 0 or idx >= len(files):
                        Utilities.print_error(f"Index {idx} out of range.")
                        continue
                    candidate = os.path.join(current_dir, files[idx])
                    if os.path.isdir(candidate):
                        current_dir = os.path.abspath(candidate)
                        print(Fore.GREEN + f"Changed directory to '{current_dir}'")
                    else:
                        Utilities.print_error(f"File at index {idx} is not a directory.")
                    continue
                candidate = os.path.join(current_dir, cmd_args[0])
                if os.path.isdir(candidate):
                    new_dir = os.path.abspath(candidate)
                else:
                    new_dir = os.path.abspath(cmd_args[0])
                if os.path.isdir(new_dir):
                    current_dir = new_dir
                    print(Fore.GREEN + f"Changed directory to '{current_dir}'")
                else:
                    Utilities.print_error(f"Directory '{new_dir}' does not exist.")
            elif cmd == "ls":
                sort_type = cmd_args[0] if cmd_args else "A-Z"
                files = os.listdir(current_dir)
                files = sort_files(files, current_dir, sort_type)
                print(Fore.CYAN + f"Files in '{current_dir}' ({sort_type}):")
                for i, f in enumerate(files):
                    full_path = os.path.join(current_dir, f)
                    size = os.path.getsize(full_path)
                    print(Fore.YELLOW + f"<{i}>", end="")
                    if os.path.isdir(full_path):
                        Utilities.print_step(Fore.WHITE + f"    {f}/ {Fore.BLUE}(dir)",0.001)
                    else:
                        Utilities.print_step(Fore.WHITE + f"    {f} {Fore.BLUE}({size} bytes)",0.001)
            elif cmd == "create":
                if not cmd_args:
                    Utilities.print_error("No filename specified.")
                    continue
                file_type = input("Enter file type (e.g., txt, py, md): ").strip()
                if not file_type:
                    Utilities.print_error("No file type specified.")
                    continue
                filename = os.path.join(current_dir, f"{cmd_args[0]}.{file_type}")
                filename = os.path.join(current_dir, cmd_args[0])
                with open(filename, "w") as f:
                    f.write(input("Content:"))
                print(Fore.GREEN + f"File '{filename}' created.")
            elif cmd == "open":
                if not cmd_args:
                    Utilities.print_error("No filename specified.")
                    continue
                if cmd_args[0].isdigit():
                    idx = int(cmd_args[0])
                    files = os.listdir(current_dir)
                    if not sort_type:
                        sort_type = "A-Z"
                    files = sort_files(files, current_dir, sort_type)
                    if idx < 0 or idx >= len(files):
                        Utilities.print_error(f"Index {idx} out of range.")
                        continue
                    filename = os.path.join(current_dir, files[idx])
                else:
                    filename = os.path.join(current_dir, cmd_args[0])
                if not os.path.isfile(filename):
                    Utilities.print_error("File does not exist.")
                    continue
                try:
                    with open(filename, "r") as f:
                        i = 1
                        for line in f:
                            print(Fore.YELLOW + f">{str(i)} ", Fore.WHITE + line.rstrip())
                            i += 1
                except Exception as e:
                    Utilities.print_error(str(e))
            elif cmd == "destroy":
                if not cmd_args:
                    Utilities.print_error("No filename specified.")
                    continue
                if cmd_args[0].isdigit():
                    idx = int(cmd_args[0])
                    files = os.listdir(current_dir)
                    if not sort_type:
                        sort_type = "A-Z"
                    files = sort_files(files, current_dir, sort_type)
                    if idx < 0 or idx >= len(files):
                        Utilities.print_error(f"Index {idx} out of range.")
                        continue
                    filename = os.path.join(current_dir, files[idx])
                elif cmd_args[0] == "all":
                    files = os.listdir(current_dir)
                    deleted_any = False
                    for f in files:
                        full_path = os.path.join(current_dir, f)
                        if os.path.isfile(full_path):
                            os.remove(full_path)
                            print(Fore.RED + f"File '{full_path}' destroyed.")
                            deleted_any = True
                    if not deleted_any:
                        print(Fore.YELLOW + "No files to delete in this directory.")
                    continue
                else:
                    filename = os.path.join(current_dir, cmd_args[0])
                if os.path.isfile(filename):
                    os.remove(filename)
                    print(Fore.RED + f"File '{filename}' destroyed.")
                else:
                    Utilities.print_error("File does not exist.")
            elif cmd == "pwd":
                print(f"Current Directory is: {current_dir}")
            else:
                Utilities.print_error("Unknown goin command.")
    except Exception as e:
        Utilities.print_error(str(e))


def show_files(args):
    try:
        directory = args[0] if args else "."
        files = os.listdir(directory)
        print(Fore.CYAN + f"Files in '{directory}':")
        for f in files:
            print(Fore.WHITE + f"    {f}")
    except Exception as e:
        Utilities.print_error(str(e))

def help():
    print(Fore.CYAN + "Available commands (purple commands are addons's commands):")
    for com in commands_av:
        print(Fore.GREEN + f"  {com['name']}" + Fore.WHITE + f" : {com['desc']}")
    from Manager import addon_commands
    for name, func in addon_commands.items():
        desc = func.__doc__ or "(no description)"
        print(Fore.MAGENTA + f"  {name}" + Fore.WHITE + f" : {desc}")

def open_file(args):
    try:
        if not args:
            Utilities.print_error("No filename provided.")
            return
        filename = args[0]
        if not os.access(filename, os.R_OK):
            Utilities.print_error("You do not have read permission for this file.")
            return
        with open(filename, "r") as f:
            i = 1
            for line in f:
                print(Fore.YELLOW + (f">{str(i)} "), Fore.WHITE + line.rstrip())
                i += 1
    except Exception as e:
        Utilities.print_error(str(e))

def echo(args):
    try:
        print(" ".join(args))
    except Exception as e:
        Utilities.print_error(str(e))

def add(args):
    try:
        if len(args) < 2:
            Utilities.print_error("Please provide two numbers.")
            return
        a, b = float(args[0]), float(args[1])
        print(Fore.LIGHTBLUE_EX + f"Result: {a + b}")
    except Exception as e:
        Utilities.print_error(str(e))

def mkdir(args):
    try:
        if not args:
            Utilities.print_error("No directory name specified.")
            return
        os.makedirs(args[0], exist_ok=True)
        print(Fore.GREEN + f"Directory '{args[0]}' created.")
    except Exception as e:
        Utilities.print_error(str(e))

def rmdir(args):
    try:
        if not args:
            Utilities.print_error("No directory name specified.")
            return
        os.rmdir(args[0])
        print(Fore.GREEN + f"Directory '{args[0]}' removed.")
    except Exception as e:
        Utilities.print_error(str(e))

def rename(args):
    try:
        if len(args) < 2:
            Utilities.print_error("Usage: rename <src> <dst>")
            return
        os.rename(args[0], args[1])
        print(Fore.GREEN + f"Renamed '{args[0]}' to '{args[1]}'")
    except Exception as e:
        Utilities.print_error(str(e))

def copy(args):
    try:
        import shutil
        if len(args) < 2:
            Utilities.print_error("Usage: copy <src> <dst>")
            return
        shutil.copy2(args[0], args[1])
        print(Fore.GREEN + f"Copied '{args[0]}' to '{args[1]}'")
    except Exception as e:
        Utilities.print_error(str(e))

def move(args):
    try:
        import shutil
        if len(args) < 2:
            Utilities.print_error("Usage: move <src> <dst>")
            return
        shutil.move(args[0], args[1])
        print(Fore.GREEN + f"Moved '{args[0]}' to '{args[1]}'")
    except Exception as e:
        Utilities.print_error(str(e))

def cat(args):
    try:
        if not args:
            Utilities.print_error("No filename specified.")
            return
        with open(args[0], "r") as f:
            print(f.read())
    except Exception as e:
        Utilities.print_error(str(e))

def touch(args):
    try:
        if not args:
            Utilities.print_error("No filename specified.")
            return
        with open(args[0], "a"):
            os.utime(args[0], None)
        print(Fore.GREEN + f"File '{args[0]}' touched/created.")
    except Exception as e:
        Utilities.print_error(str(e))

def whoami(args):
    try:
        import getpass
        print(getpass.getuser())
    except Exception as e:
        Utilities.print_error(str(e))

def date(args):
    try:
        from datetime import datetime
        print(datetime.now())
    except Exception as e:
        Utilities.print_error(str(e))

def sort_files(files, current_dir, sort_type="A-Z"):
    if sort_type == "A-Z":
        files.sort()
    elif sort_type == "Z-A":
        files.sort(reverse=True)
    elif sort_type == "heaviest":
        files.sort(key=lambda f: os.path.getsize(os.path.join(current_dir, f)), reverse=True)
    elif sort_type == "lightest":
        files.sort(key=lambda f: os.path.getsize(os.path.join(current_dir, f)))
    elif sort_type == "type":
        files.sort(key=lambda f: os.path.splitext(f)[1])
    elif sort_type == "folder":
        files[:] = [f for f in files if os.path.isdir(os.path.join(current_dir, f))]
    elif sort_type == "file":
        files[:] = [f for f in files if os.path.isfile(os.path.join(current_dir, f))]
    elif sort_type.startswith("."):
        ext = sort_type
        files[:] = [f for f in files if os.path.isfile(os.path.join(current_dir, f)) and f.endswith(ext)]
    else:
        files.sort()
    return files

def reload_addons(args=None):
    try:
        from Manager import load_addons
        load_addons()
        print(Fore.GREEN + "Addons reloaded!")
    except Exception as e:
        Utilities.print_error(f"Failed to reload addons: {e}")
