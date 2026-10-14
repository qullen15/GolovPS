import os
import socket


def parse_command(line):
    parts = line.split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def main():
    username = os.environ.get("USER") or os.environ.get("USERNAME")
    hostname = socket.gethostname()

    while True:
        prompt = f"{username}@{hostname}:~$ "
        user_input = input(prompt)

        command, args = parse_command(user_input)
        if command is None:
            continue

        if command == "exit":
            break
        elif command == "ls":
            print(f"Команда: ls, аргументы: {' '.join(args)}")
        elif command == "cd":
            print(f"Команда: cd, аргументы: {' '.join(args)}")
        else:
            print(f"{command}: команда не найдена")


if __name__ == "__main__":
    main()