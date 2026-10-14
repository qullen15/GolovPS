import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import parse_command


class TestParser(unittest.TestCase):
    def test_parse_simple(self):
        command, args = parse_command("ls -l")
        self.assertEqual(command, "ls")
        self.assertEqual(args, ["-l"])

    def test_parse_empty(self):
        command, args = parse_command("")
        self.assertIsNone(command)
        self.assertEqual(args, [])

    def test_parse_no_args(self):
        command, args = parse_command("exit")
        self.assertEqual(command, "exit")
        self.assertEqual(args, [])


if __name__ == "__main__":
    unittest.main()