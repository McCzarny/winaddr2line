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
            "D:\\a\\winaddr2line\\winaddr2line\\testing_binary\\src\\"
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

        self.assertEqual(
            result.returncode,
            0,
            f"Command failed. Output:\n{result.stdout}\nStdErr:\n{result.stderr}",
        )
        self.assertEqual(
            result.stdout.strip(), expected_output.strip(), "Output mismatch"
        )

    def test_line_main_start(self):
        self.run_expecting_success(
            [*self.line_args, "0x1000"], f"{self.src_path}testApp.cpp:42"
        )

    def test_line_with_symbol_main_start(self):
        self.run_expecting_success(
            [*self.line_with_symbol_args, "0x1000"], f"main\n{self.src_path}testApp.cpp:42"
        )

    def test_line_main_middle(self):
        self.run_expecting_success(
            [*self.line_args, "0x10C4"], f"{self.src_path}testApp.cpp:46"
        )

    def test_line_with_symbol_main_middle(self):
        self.run_expecting_success(
            [*self.line_with_symbol_args, "0x10C4"], f"main\n{self.src_path}testApp.cpp:46"
        )

    def test_line_main_no_prefix(self):
        self.run_expecting_success(
            [*self.line_args, "1000"], f"{self.src_path}testApp.cpp:42"
        )
    
    def test_line_with_symbol_main_no_prefix(self):
        self.run_expecting_success(
            [*self.line_with_symbol_args, "1000"], f"main\n{self.src_path}testApp.cpp:42"
        )

    def test_line_lambda(self):
        self.run_expecting_success(
            [*self.line_args, "0x2800"], f"{self.src_path}testApp.cpp:31"
        )

    def test_line_with_symbol_lambda(self):
        lambda_name = "TextExtractor::processTexts<<lambda_de390742b4447c477e4e7f2e67523fc2> >"
        self.run_expecting_success(
            [*self.line_with_symbol_args, "0x2800"], f"{lambda_name}\n{self.src_path}testApp.cpp:31"
        )

    def test_line_member_function(self):
        self.run_expecting_success(
            [*self.line_args, "0x3EA0"], f"{self.src_path}testApp.cpp:24"
        )

    def test_line_with_symbol_member_function(self):
        member_function_name = "TextExtractor::printTexts"
        self.run_expecting_success(
            [*self.line_with_symbol_args, "0x3EA0"], f"{member_function_name}\n{self.src_path}testApp.cpp:24"
        )

    def test_line_multiple_addresses(self):
        self.run_expecting_success(
            [*self.line_args, "0x1000", "0x1050", "0x1100"],
            "\n".join([
                f"{self.src_path}testApp.cpp:42",
                f"{self.src_path}testApp.cpp:44",
                f"{self.src_path}testApp.cpp:46",
            ]),
        )

    def test_line_with_symbol_multiple_addresses(self):
        self.run_expecting_success(
            [*self.line_with_symbol_args, "0x1000", "0x1050", "0x3EA0"],
            "\n".join([
                "main",
                f"{self.src_path}testApp.cpp:42",
                "main",
                f"{self.src_path}testApp.cpp:44",
                "TextExtractor::printTexts",
                f"{self.src_path}testApp.cpp:24",
            ]),
        )

if __name__ == "__main__":
    if not os.getenv("WINADDR2LINE_PATH"):
        print("WINADDR2LINE_PATH environment variable is not set")
        exit(1)
    unittest.main()
