import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import build_parser, execute_command, run_script, main


class TestBuildParser:
    """Разбор аргументов командной строки."""

    def test_parses_vfs_and_script(self):
        args = build_parser().parse_args(
            ["--vfs", "data/vfs.img", "--script", "scripts/demo.start"])
        assert args.vfs == "data/vfs.img"
        assert args.script == "scripts/demo.start"

    def test_defaults_when_no_args(self):
        args = build_parser().parse_args([])
        assert args.vfs is None
        assert args.script is None

    def test_unknown_argument_exits_with_code_2(self):
        with pytest.raises(SystemExit) as exc:
            build_parser().parse_args(["--unknown"])
        assert exc.value.code == 2


class TestExecuteCommand:
    """Выполнение одной команды: успех = None, ошибка = строка."""

    def test_stub_ls_prints_name_and_args(self, capsys):
        result = execute_command("ls", ["-l", "/home"])
        out = capsys.readouterr().out
        assert "Команда: ls" in out
        assert "-l /home" in out
        assert result is None

    def test_stub_cd_prints_name_and_args(self, capsys):
        result = execute_command("cd", ["docs"])
        out = capsys.readouterr().out
        assert "Команда: cd" in out
        assert "docs" in out
        assert result is None

    def test_unknown_command_returns_error_string(self, capsys):
        result = execute_command("ping", ["pong"])
        out = capsys.readouterr().out
        assert result is not None
        assert "команда не найдена" in result
        assert out == ""


class TestRunScript:
    """Выполнение стартового скрипта."""

    def test_success_script_returns_zero(self, tmp_path, capsys):
        script = tmp_path / "ok.start"
        script.write_text("ls -l /home\ncd docs\nexit\n", encoding="utf-8")
        assert run_script(str(script), "") == 0

    def test_stops_on_first_error(self, tmp_path, capsys):
        script = tmp_path / "fail.start"
        script.write_text("ls\nping pong\nls\n", encoding="utf-8")
        code = run_script(str(script), "")
        out = capsys.readouterr().out
        assert code == 1
        assert "работа остановлена" in out
        assert out.count("Команда: ls") == 1

    def test_missing_script_returns_one(self, tmp_path, capsys):
        code = run_script(str(tmp_path / "nope.start"), "")
        out = capsys.readouterr().out
        assert code == 1
        assert "Ошибка" in out


class TestMain:
    """Точка входа: main() завершает процесс через SystemExit(код)."""

    def test_debug_output_lists_parameters(self, tmp_path, capsys, monkeypatch):
        script = tmp_path / "demo.start"
        script.write_text("exit\n", encoding="utf-8")
        monkeypatch.setattr(
            sys, "argv",
            ["main.py", "--vfs", "data/vfs.img", "--script", str(script)])
        with pytest.raises(SystemExit) as exc:
            main()
        out = capsys.readouterr().out
        assert exc.value.code == 0
        assert "[debug] путь к VFS: data/vfs.img" in out
        assert "[debug] путь к стартовому скрипту:" in out

    def test_debug_output_when_vfs_not_set(self, tmp_path, capsys, monkeypatch):
        script = tmp_path / "demo.start"
        script.write_text("exit\n", encoding="utf-8")
        monkeypatch.setattr(
            sys, "argv", ["main.py", "--script", str(script)])
        with pytest.raises(SystemExit) as exc:
            main()
        out = capsys.readouterr().out
        assert exc.value.code == 0
        assert "путь к VFS: не задан" in out

    def test_main_propagates_script_error_code(self, tmp_path, capsys, monkeypatch):
        script = tmp_path / "fail.start"
        script.write_text("ping pong\n", encoding="utf-8")
        monkeypatch.setattr(
            sys, "argv", ["main.py", "--script", str(script)])
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1