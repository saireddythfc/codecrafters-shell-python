import sys


def main():
    # Uncomment this block to pass the first stage
    valid = ["exit", "echo", "type"]
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()

        if command == "exit 0":
            break
        elif command[:5] == "echo ":
            print(command[5:])
        elif command[:5] == "type ":
            if command[5:] in valid:
                print(f"{command[5:]} is a shell builtin")
            else:
                print(f"{command[5:]}: not found")
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
