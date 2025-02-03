import sys
import os


def main():
    # Uncomment this block to pass the first stage
    valid = ["exit", "echo", "type", "ls", "cat"]
    path = os.environ.get("PATH")

    idx = path.find(":")
    dir_path = path[idx + 1 :] + "/"

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
            words = command[5:].split()
            if words[0] in valid:
                if len(path) > 0:
                    dir_path = dir_path + words[0]
                    sys.stdout.write(f"{words[0]} is {dir_path}" + "\n")
                else:
                    sys.stdout.write(f"{command[5:]} is a shell builtin" + "\n")
            else:
                sys.stdout.write(f"{command[5:]}: not found" + "\n")

        else:
            sys.stdout.write(f"{command}: command not found" + "\n")

        sys.stdout.flush()


if __name__ == "__main__":
    main()
