import sys
import os
import shutil
from pathlib import Path
import shlex
import readline


def find_executables(paths=None):
    """Finds all executable files in the specified paths (or PATH if None)."""

    if paths is None:
        paths = os.environ["PATH"].split(os.pathsep)  # Use the system's PATH

    executables = set()  # Use a set to avoid duplicates

    for path in paths:
        if os.path.isdir(path):  # Check if it's a directory
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)

                if os.path.isfile(filepath) and os.access(
                    filepath, os.X_OK
                ):  # Check if it's a file and executable
                    executables.add(filename)
                # Check for executables without extension on some systems
                elif (
                    os.path.isfile(filepath)
                    and not os.path.splitext(filename)[1]
                    and os.access(filepath, os.X_OK)
                ):
                    executables.add(filename)

    return sorted(list(executables))  # Return sorted list for consistent order


def display_matches(substitution, matches, longest_match_length):
    try:
        sys.stdout.write("\n")
        sys.stdout.write(" ".join(matches) + "\n")
        sys.stdout.write(f"$ {substitution}")
        sys.stdout.flush()
        readline.redisplay()  # type: ignore
    except Exception as e:
        sys.stderr.write(f"{e}")


def completer(text, state):
    execs = find_executables()
    commands = ["exit ", "echo ", "type ", "pwd ", "cd "]
    matches = [cmd for cmd in commands if cmd.startswith(text)]

    if state >= len(matches):
        exes = [exe for exe in execs if exe.startswith(text)]
        return exes[state] + " " if state < len(exes) else None

    return matches[state] if state < len(matches) else None


def main():

    valid = ["exit", "echo", "type", "pwd", "cd"]
    type_valid = ["ls", "cat", "cp", "mkdir", "my_exe"]
    PATH = os.environ.get("PATH")
    HOME = os.getenv("HOME")

    working_dir = os.getcwd()

    readline.set_completion_display_matches_hook(display_matches)
    readline.parse_and_bind("set bell-style audible")
    readline.set_auto_history(True)
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    while True:

        PATH = os.environ.get("PATH")
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        command = input()
        cmds = command.split()

        args = shlex.split(command)
        cmd, args = args[0], args[1:]

        if command == "exit 0":
            break

        if cmd == "echo":

            if "1>>" in args or ">>" in args:
                op_file_path = args[-1]
                output = args[0]
                f = open(op_file_path, "a")
                f.write(output + "\n")
                f.close()

            elif "1>" in args or ">" in args:
                op_file_path = args[-1]
                output = args[0]

                f = open(op_file_path, "w")
                f.write(output + "\n")
                f.close()

            else:
                if "2>" in args or "2>>" in args:
                    output = args[0]
                    op_file_path = args[-1]
                    f = open(op_file_path, "w")
                    f.write("")
                    f.close()

                else:
                    output = " ".join(args)
                sys.stdout.write(f"{output}" + "\n")

        elif cmd == "type":
            PATH = os.getenv("PATH")
            word = command[5:].split()[0]

            paths = PATH.split(":")
            for path in paths:
                if os.path.exists(f"{path}/{word}"):
                    cmd_path = f"{path}/{word}"
                    break

            if word in type_valid:
                if cmd_path:
                    sys.stdout.write(f"{word} is {cmd_path}" + "\n")
                else:
                    sys.stdout.write(f"{word}: not found" + "\n")

            elif word in valid:
                sys.stdout.write(f"{word} is a shell builtin" + "\n")

            else:
                sys.stdout.write(f"{word}: not found" + "\n")

        elif cmd == "pwd":

            if working_dir:
                sys.stdout.write(f"{working_dir}" + "\n")
            else:
                sys.stdout.write(f"{working_dir}" + "\n")

        elif cmd == "cd":

            if cmds[1] == "~":
                HOME = os.getenv("HOME")

                homes = HOME.split(":")
                for home in homes:
                    if os.path.exists(f"{home}"):
                        working_dir = f"{home}"
                        break

            else:
                try:
                    dirs = cmds[1].split("/")
                    if "." in dirs[0]:
                        current_directory = Path(working_dir)
                        relative_path = Path(cmds[1])
                        absolute_path = (current_directory / relative_path).resolve()
                        working_dir = str(absolute_path)
                    else:
                        os.chdir(" ".join(cmds[1:]))
                        working_dir = cmds[1]
                except FileNotFoundError:
                    working_dir = os.getcwd()
                    sys.stdout.write(f"cd: {cmds[1]}: No such file or directory" + "\n")

        elif "exe " in cmd:
            file = open(args[0], "r")
            sys.stdout.write(f"{file.read()}")
            file.close()

        else:
            exe = command.split()[0]
            check = shutil.which(exe)

            if check and os.access(check, os.X_OK):
                os.system(command)
            else:
                sys.stdout.write(f"{command}: command not found" + "\n")

        sys.stdout.flush()

    sys.stdout.close()


if __name__ == "__main__":
    main()
