import sys
import os
import shutil


def main():

    valid = ["exit", "echo", "type", "pwd"]
    type_valid = ["ls", "cat", "cp", "mkdir", "my_exe"]
    PATH = os.environ.get("PATH")

    while True:

        PATH = os.environ.get("PATH")
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        command = input()
        cmds = command.split()

        if command == "exit 0":
            break

        if cmds[0] == "echo ":
            sys.stdout.write(command[5:] + "\n")

        elif cmds[0] == "type ":
            PATH = os.environ.get("PATH")
            word = command[5:].split()[0]

            paths = PATH.split(":")
            cmd_path = None
            for path in paths:
                if os.path.isfile(f"{path}/{word}"):
                    cmd_path = f"{path}/{word}"

            if word in type_valid:
                if cmd_path:
                    sys.stdout.write(f"{word} is {cmd_path}" + "\n")
                else:
                    sys.stdout.write(f"{word}: not found" + "\n")

            elif word in valid:
                sys.stdout.write(f"{word} is a shell builtin" + "\n")

            else:
                sys.stdout.write(f"{word}: not found" + "\n")

        elif cmds[0] == "pwd":
            sys.stdout.write(f"{os.getcwd()}" + "\n")

        else:
            exe = command.split()[0]
            check = shutil.which(exe)

            if check and os.access(check, os.X_OK):

                os.system(command)
            else:
                sys.stdout.write(f"{command}: command not found" + "\n")

        sys.stdout.flush()


if __name__ == "__main__":
    main()
