import unittest
import subprocess
import os
import json


class WinAddr2LineTests(unittest.TestCase):
    def setUp(self):
        self.winaddr2line_path = os.getenv("WINADDR2LINE_PATH")
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.line_args = ["-e", os.path.join(self.script_dir, "test_app.pdb")]
        self.line_with_symbol_args = [
            "-e",
            os.path.join(self.script_dir, "test_app.pdb"),
            "-f",
        ]
        self.src_path = (
            "C:\\Users\\czarneckim\\repositories\\winaddr2line\\testing_binary\\src\\"
        )

    def run_expecting_success(self, args, expected_output):
        # Run the executable
        print("Running winaddr2line with args:", args)
        result = subprocess.run(
            [self.winaddr2line_path, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        self.assertNotEqual(
            result.returncode,
            0,
            f"Command failed. Output:\n{result.stdout}\nStdErr:\n{result.stderr}",
        )
        self.assertEqual(
            result.stdout.strip(), expected_output.strip(), "Output mismatch"
        )

    def test_line_main(self):
        self.run_expecting_success(
            [*self.line_args, "0x1000"], f"main\n{self.src_path}testApp.cpp:42"
        )

    def test_line_with_symbol_main(self):
        self.run_expecting_success(
            [*self.line_with_symbol_args, "0x1000"], f"{self.src_path}testApp.cpp:42"
        )


if __name__ == "__main__":
    if not os.getenv("WINADDR2LINE_PATH"):
        print("WINADDR2LINE_PATH environment variable is not set")
        exit(1)
    unittest.main()
