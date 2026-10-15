import argparse
import os
import socket


def build_parser():
    """Создаёт парсер параметров командной строки эмулятора."""

    parser = argparse.ArgumentParser(
        prog="vfs-shell",
        description="Эмулятор командной строки UNIX-подобной ОС.",
    )

    parser.add_argument("--vfs", metavar="PATH", default=None,
                        help="путь к физическому расположению VFS")
    
    parser.add_argument("--script", metavar="PATH", default=None,
                        help="путь к стартовому скрипту с командами эмулятора")
    
    return parser


def print_debug(args):
    """Печатает отладочный вывод всех заданных параметров запуска."""

    vfs = args.vfs if args.vfs is not None else "не задан"
    script = args.script if args.script is not None else "не задан"
    
    print(f"[debug] путь к VFS: {vfs}")
    print(f"[debug] путь к стартовому скрипту: {script}")


def parse_command(line):
    """Разбирает строку ввода на команду и список аргументов."""

    parts = line.split()

    if not parts:
        return None, []
    
    return parts[0], parts[1:]


def execute_command(command, args):
    """Выполняет команду эмулятора."""

    if command == "ls":
        print(f"Команда: ls, аргументы: {' '.join(args)}")
    elif command == "cd":
        print(f"Команда: cd, аргументы: {' '.join(args)}")
    else:
        return f"{command}: команда не найдена"
    
    return None


def run_script(path, prompt):
    """Выполняет команды стартового скрипта, имитируя диалог с пользователем."""

    try:
        with open(path, encoding="utf-8") as script_file:
            lines = script_file.read().splitlines()

    except OSError as exc:
        print(f"Ошибка стартового скрипта: {exc}")
        return 1
    
    for line in lines:
        line = line.strip()

        if not line:
            continue
        print(f"{prompt}{line}")

        command, args = parse_command(line)

        if command is None:
            continue

        if command == "exit":
            return 0
        
        error = execute_command(command, args)
        if error is not None:
            print(error)
            print("Ошибка выполнения стартового скрипта: работа остановлена")
            return 1
    return 0


def main():
    """Точка входа: разбор параметров, отладочный вывод, выбор режима."""

    args = build_parser().parse_args()
    print_debug(args)

    username = os.environ.get("USER") or os.environ.get("USERNAME")
    hostname = socket.gethostname()
    prompt = f"{username}@{hostname}:~$ "

    if args.script is not None:
        raise SystemExit(run_script(args.script, prompt))

    while True:
        user_input = input(prompt)
        command, cmd_args = parse_command(user_input)

        if command is None:
            continue
        if command == "exit":
            break

        error = execute_command(command, cmd_args)
        if error is not None:
            print(error)


if __name__ == "__main__":
    main()