import sys


def main():
    # Uncomment this block to pass the first stage
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()

        if command == "exit 0":
            break
        elif command[:5] == "echo ":
            print(command[5:])
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
