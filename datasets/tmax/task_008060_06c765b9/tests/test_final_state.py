# test_final_state.py

import os
import subprocess
import tempfile

def test_c_program_exists():
    c_prog_path = "/home/user/clean_logs.c"
    assert os.path.isfile(c_prog_path), f"C program not found at {c_prog_path}"

def test_c_program_functionality():
    c_prog_path = "/home/user/clean_logs.c"
    assert os.path.isfile(c_prog_path), f"Cannot test functionality: {c_prog_path} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        exe_path = os.path.join(tmpdir, "clean_logs")

        # Compile the C program
        compile_proc = subprocess.run(["gcc", c_prog_path, "-o", exe_path], capture_output=True, text=True)
        assert compile_proc.returncode == 0, f"Failed to compile {c_prog_path}. Error:\n{compile_proc.stderr}"

        # Create a dummy log file
        input_log = os.path.join(tmpdir, "input.log")
        output_log = os.path.join(tmpdir, "output.log")

        test_content = (
            "[DEBUG] This is a debug line\n"
            "[INFO] This is an info line\n"
            "This is a normal line\n"
            "[DEBUG] Another debug line\n"
            "[WARNING] Watch out\n"
        )

        with open(input_log, "w") as f:
            f.write(test_content)

        # Run the compiled program
        run_proc = subprocess.run([exe_path, input_log, output_log], capture_output=True, text=True)
        assert run_proc.returncode == 0, f"Execution of compiled C program failed. Error:\n{run_proc.stderr}"

        assert os.path.isfile(output_log), "The C program did not create the expected output file."

        with open(output_log, "r") as f:
            out_content = f.read()

        expected_out_content = (
            "[INFO] This is an info line\n"
            "This is a normal line\n"
            "[WARNING] Watch out\n"
        )

        assert out_content == expected_out_content, (
            "The C program did not correctly filter the log file. "
            f"Expected:\n{expected_out_content}\nGot:\n{out_content}"
        )

def test_report_exists():
    report_path = "/home/user/space_saved.txt"
    assert os.path.isfile(report_path), f"Report file not found at {report_path}"

def test_report_content():
    report_path = "/home/user/space_saved.txt"
    assert os.path.isfile(report_path), f"Cannot verify content: {report_path} does not exist."

    # Try to read the expected value from the setup's hidden file, fallback to known truth
    expected_val_path = "/tmp/expected_saved.txt"
    if os.path.isfile(expected_val_path):
        with open(expected_val_path, "r") as f:
            expected_bytes = f.read().strip()
    else:
        # Fallback to the derived truth value from the prompt
        expected_bytes = "619500"

    expected_line = f"Bytes saved: {expected_bytes}"

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == expected_line, (
        f"Report content is incorrect.\n"
        f"Expected exactly: '{expected_line}'\n"
        f"Found: '{content}'"
    )