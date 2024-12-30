import subprocess
import os
import json

def test_success(winaddr2line_path, args, expected_output):
    # Run the executable
    print("Running winaddr2line with args:", args)
    result = subprocess.run([winaddr2line_path, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Check the return code
    if result.returncode != 0:
        print("Test failed")
        print("Output:", result.stdout)
        print("Error:", result.stderr)
        return False
    
    # Check the output
    if result.stdout.strip() == expected_output.strip():
        print("Test passed")
        return True
    else:
        print("Test failed")
        print(f"Expected:\n{expected_output}")
        print(f"Got:\n{result.stdout}")
        print("Error:", result.stderr)
        return False


def run_test(winaddr2line_path):
    print("Running test")
    print("Exec directory:", winaddr2line_path)
    
    failed_tests = []
    passed_tests = []

    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_path = os.path.join(script_dir, "test_data.json")
    with open(test_data_path, "r") as f:
        test_data = json.load(f)
    
    # Test line only mode
    for test in test_data:
        args = ["-e", os.path.join(script_dir, "test_app.pdb"), test["input_address"]]
        if test_success(winaddr2line_path, args, test["expected_line"]):
            passed_tests.append(test)
        else:
            failed_tests.append(test)

    # Test line and symbol mode
    for test in test_data:
        args = ["-e", os.path.join(script_dir, "test_app.pdb"), test["input_address"], "-f"]
        if test_success(winaddr2line_path, args, f"{test['expected_symbol']}\n{test['expected_line']}"):
            passed_tests.append(test)
        else:
            failed_tests.append(test)

    print("Tests passed:", len(passed_tests))
    print("Tests failed:", len(failed_tests))
        
    if len(failed_tests) > 0 or len(passed_tests) == 0:
        print("Test failed")
        return False
    
    return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run tests for winaddr2line")
    parser.add_argument("winaddr2line_path", help="Path to winaddr2line executable")
    args = parser.parse_args()
    if not run_test(args.winaddr2line_path):
        exit(1)
    

