import time as tm
import math
import sys
import random as rd
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

class MazeGen:
    @staticmethod
    def gen_maze(n, percent_prob):
        maze = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if rd.randint(0, 100) <= percent_prob:
                    maze[i][j] = 1
                else:
                    maze[i][j] = 0

        # Ensure all 0s are connected
        visited = [[False for _ in range(n)] for _ in range(n)]

        def dfs(x, y):
            if x < 0 or x >= n or y < 0 or y >= n or visited[x][y] or maze[x][y] == 1:
                return
            visited[x][y] = True
            maze[x][y] = 0
            dfs(x + 1, y)
            dfs(x - 1, y)
            dfs(x, y + 1)
            dfs(x, y - 1)

        # Start DFS from the top-left corner
        dfs(0, 0)

        # Ensure all unvisited 0s are converted to 1s
        for i in range(n):
            for j in range(n):
                if not visited[i][j] and maze[i][j] == 0:
                    maze[i][j] = 1

        return maze

class Chrono:
    def __init__(self):
        self._start_time = None
        self._elapsed = 0
        self._running = False
        self._paused = False
        self._stopped = False

    def start(self):
        if not self._running:
            self._start_time = tm.time()
            self._running = True
            self._paused = False
            self._stopped = False

    def pause(self):
        if self._running and not self._paused:
            self._elapsed += tm.time() - self._start_time
            self._paused = True
            self._running = False

    def replay(self):
        if self._paused:
            self._start_time = tm.time()
            self._running = True
            self._paused = False

    def stop(self):
        if self._running or self._paused:
            if self._running:
                self._elapsed += tm.time() - self._start_time
            self._running = False
            self._paused = False
            self._stopped = True

    def get_time(self, rounding=True):
        if self._running:
            if rounding:
                return round(self._elapsed + (tm.time() - self._start_time), 1)
            else:
                return self._elapsed + (tm.time() - self._start_time)
        else:
            elapsed = self._elapsed
            if self._stopped:
                self.re_init()
            if rounding:
                return round(elapsed, 1)
            else:
                return elapsed

    def re_init(self):
        self._start_time = None
        self._elapsed = 0
        self._running = False
        self._paused = False
        self._stopped = False
@staticmethod

def pause(t):
    remaining = t
    while remaining > 0:

        duration = min(1 / len(str(remaining)), remaining)
        tm.sleep(duration)
        remaining -= duration


def charge(message_start, time=3, speed=1, max=3, message_end=".", erase=True):
    """
    Shows an animated loading message in the console.

    Args:
        message_start (str): Message to display before the animation.
        time (int,optional): Total duration in seconds (default: 3).
        speed (int,optional): Seconds between animation steps (default: 1).
        max (int,optional): Number of animation characters per cycle (default: 3).
        message_end (str,optional): Animation character (default: ".").
        erase (bool,optional): Erase message after completion (default: True).
    """
    omax = max
    print(message_start, end="")

    while time > 0:
        while max != 0:
            time -= speed
            tm.sleep(speed)
            print(message_end, end="",flush=True)
            max -= 1
        tm.sleep(speed)
        sys.stdout.write('\r' + ' ' * (len(message_start) + omax * len(message_end)))
        sys.stdout.flush()

        sys.stdout.write('\r' + message_start)
        sys.stdout.flush()

        max = omax  # Réinitialiser max pour la prochaine itération
    if erase:
        sys.stdout.write('\r' + "\033[K")
        sys.stdout.flush()

def print_list(lst): #Print lists but in pretty way
    for item in lst:
        print(item, end='')
    print()

def look_and_say(n, iterations, printing=True): #look and say (ex:1->1x1->11->2x1->21...) : you input a list with your.s number.s and the number of iterations you want to do 
    if printing:
        print_list(n)
    for _ in range(iterations):
        result = []
        i = 0
        while i < len(n):
            count = 1
            while i + 1 < len(n) and n[i] == n[i + 1]:
                count += 1
                i += 1
            result.append(count)
            result.append(n[i])
            i += 1
        n = result
        if printing:
            print_list(n)
        else:
            return n

def var_to_list(var,do_strip=False,low=False,upp=False):
    """
    Converts a variable to a list of its elements/characters.

    Args:
        var (Any): The variable to be converted into a list.
        do_strip (bool, optional): If True and var is a string, strips whitespace before converting. Defaults to False.
        low (bool, optional): If True and var is a string, converts to lowercase before converting. Defaults to False.
        upp (bool, optional): If True and var is a string, converts to uppercase before converting. Defaults to False.
            Note: If both low and upp are True, lowercase takes priority.

    Returns:
        list: The variable converted to a list.
    """
    new_list=[]
    if isinstance(var, str):
        if do_strip:
            var=var.strip()
        if low:
            var=var.lower()
        elif upp:
            var=var.upper()
    for i in var:
        new_list.append(i)
    return new_list

def lst_to_var(lst, join_str="", do_strip=False, low=False, upp=False):
    """
    Converts a list of elements to a single variable (string by default).

    Args:
        lst (list): The list to convert.
        join_str (str, optional): String to join elements with (default: "").
        do_strip (bool, optional): If True, strips whitespace from each element before joining.
        low (bool, optional): If True, converts each element to lowercase before joining.
        upp (bool, optional): If True, converts each element to uppercase before joining.
            Note: If both low and upp are True, lowercase takes priority.

    Returns:
        str: The joined string.
    """
    def process_elem(e):
        s = str(e)
        if do_strip:
            s = s.strip()
        if low:
            s = s.lower()
        elif upp:
            s = s.upper()
        return s

    return join_str.join(process_elem(i) for i in lst)

def abs(n):
    return n*-1 if n<0 else n

def decompte(char=["3","2","1"],speed=1,do_end=True,do_space=True,space=" "):
    for i in range(len(char)):
        sys.stdout.write(char[i])
        sys.stdout.flush()
        if do_space and i < len(char) - 1:
            sys.stdout.write(space)
            sys.stdout.flush()
        tm.sleep(speed)
    if do_end:
        print()

def clear(terminal=False):
    if terminal:
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        # Efface la ligne courante et replace le curseur au début
        sys.stdout.write('\r\033[K')
        sys.stdout.flush()

def print_step(message, speed=0.5, do_end=True, randomness=0):
    randomness = max(0, randomness)
    for i in message:
        nspeed = max(0, speed + rd.uniform(-randomness, randomness))
        sys.stdout.write(i)
        sys.stdout.flush()
        tm.sleep(nspeed)
    if do_end:
        print()

def print_error(prompt):
    print(Fore.RED+ f"Error:{prompt}")

alphabet = "abcdefghijklmnopqrstuvwxyz"
character = "".join([chr(i) for i in range(32, 127)])