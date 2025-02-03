import sys


def main():
    # Uncomment this block to pass the first stage
    valid = ["exit", "echo", "type", "ls"]
    path = ""

    args = sys.argv

    for arg in args:
        if arg[:5] == "PATH=":
            idx = arg.find(":")
            path = arg[idx + 1 :]

    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()

        if command == "exit 0":
            break
        elif command[:5] == "echo ":
            print(command[5:])
        elif command[:5] == "type ":
            words = command[5:].split()
            if words[0] in valid:
                if len(path) > 0:
                    dirPath = path + "/" + words[0]
                    print(f"{words[0]} is {dirPath}")
                else:
                    print(f"{command[5:]} is a shell builtin")
            else:
                print(f"{command[5:]}: not found")
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
