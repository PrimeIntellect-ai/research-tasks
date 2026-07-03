# test_final_state.py
import os
import json
import subprocess

def test_bug_report_exists_and_valid():
    report_path = "/home/user/bug_report.json"
    assert os.path.isfile(report_path), f"Bug report {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} is not valid JSON."

    assert "bad_commit_hash" in report, "Missing 'bad_commit_hash' in bug report."
    assert "buggy_function_name" in report, "Missing 'buggy_function_name' in bug report."
    assert "decoded_payload_length" in report, "Missing 'decoded_payload_length' in bug report."

    # Verify buggy_function_name
    assert report["buggy_function_name"] == "process_tlv", "Incorrect 'buggy_function_name' in bug report."

    # Verify decoded_payload_length
    assert report["decoded_payload_length"] == 53, "Incorrect 'decoded_payload_length' in bug report."

    # Verify bad_commit_hash
    # Find the commit hash for "Optimize metadata processing"
    repo_dir = "/home/user/tlv_processor"
    result = subprocess.run(
        ["git", "log", "--all", "--grep=Optimize metadata processing", "--format=%H"],
        cwd=repo_dir, capture_output=True, text=True
    )
    expected_hash = result.stdout.strip()
    assert expected_hash, "Could not find the expected commit in the git history."
    assert report["bad_commit_hash"] == expected_hash, f"Incorrect 'bad_commit_hash'. Expected {expected_hash}, got {report['bad_commit_hash']}."

def test_decoded_output():
    output_path = "/home/user/decoded_output.txt"
    assert os.path.isfile(output_path), f"Decoded output {output_path} is missing."

    expected_output = "String: Hello\nPadding/Metadata (0 bytes)\nString: World\n"
    with open(output_path, "r") as f:
        actual_output = f.read()

    assert actual_output == expected_output, "The decoded output does not match the expected output."

def test_tlv_processor_fixed():
    repo_dir = "/home/user/tlv_processor"

    # Recompile to ensure it builds
    make_result = subprocess.run(["make"], cwd=repo_dir, capture_output=True, text=True)
    assert make_result.returncode == 0, f"Compilation failed:\n{make_result.stderr}"

    # Run the compiled program against the payload
    payload_path = "/home/user/payload.bin"
    run_result = subprocess.run(
        ["./tlv_decoder", payload_path],
        cwd=repo_dir, capture_output=True, text=True, timeout=5
    )
    assert run_result.returncode == 0, "The tlv_decoder failed to execute successfully."

    expected_output = "String: Hello\nPadding/Metadata (0 bytes)\nString: World\n"
    assert run_result.stdout == expected_output, "The tlv_decoder output is incorrect, the bug might not be fully fixed."