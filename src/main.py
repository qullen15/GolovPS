import os
import socket

def main():
    username = os.getlogin()
    hostname = socket.gethostname()

    while True:
        prompt = f"{username}@{hostname}:~$ "
        user_input = input(prompt)

        parts = user_input.split()
        if not parts:
            continue

        command = parts[0]
        args = parts[1:]

        if command == "exit":
            break
        elif command == "ls":
            print(f"Команда: ls, аргументы: {' '.join(args)}")
        elif command == "cd":
            print(f"Команда: cd, аргументы: {' '.join(args)}")
        else:
            print(f"{command}: команда не найдена")

main()