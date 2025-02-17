import sys
import os
import shutil
import random


def main():
    # Uncomment this block to pass the first stage
    valid = ["exit", "echo", "type"]
    type_valid = ["ls", "cat", "cp", "mkdir", "my_exe"]
    PATH = os.environ.get("PATH")

    # idx = path.find(":")
    # dir_path = path[idx + 1 :] + "/"

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        # Wait for user input
        command = input()

        if command == "exit 0":
            break

        if command[:5] == "echo ":
            sys.stdout.write(command[5:] + "\n")

        elif command[:5] == "type ":
            word = command[5:].split()[0]

            paths = PATH.split(":")
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

        else:
            # sys.stdout.write(f"{command}: command not found" + "\n")
            exe = command.split()[0]
            # check = shutil.which(exe)
            # if check and os.access(check, os.X_OK):
            #     args = command.split()
            #     sys.stdout.write(
            #         f"Program was passed {len(args)} args (including program name)."
            #         + "\n"
            #     )
            #     sys.stdout.write(f"Arg #0 (program name): {args[0]}" + "\n")
            #     for i in range(len(args) - 1):
            #         sys.stdout.write(f"Arg #{i+1}: {args[i+1]}" + "\n")
            #     random_number = random.randint(10**9, 10**10 - 1)
            #     sys.stdout.write(f"Program Signature: {random_number}" + "\n")
            # else:
            #     sys.stdout.write(f"{command}: command not found")

            os.system(exe)

        sys.stdout.flush()


if __name__ == "__main__":
    main()
