# test_final_state.py

import os
import subprocess
import pytest

CORRUPTED_STRING = "ID:8992|TEMP:12.4|STATUS:WARN|CORRUPT_FIELD_NO_COLON"

def test_corrupted_string_extracted():
    file_path = "/home/user/corrupted_string.txt"
    assert os.path.isfile(file_path), f"{file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read().strip()
    assert content == CORRUPTED_STRING, f"Expected {file_path} to contain '{CORRUPTED_STRING}', but got '{content}'"

def test_processor_test_exists_and_contains_string():
    test_file = "/home/user/processor/processor_test.go"
    assert os.path.isfile(test_file), f"{test_file} is missing. You need to write a regression test."
    with open(test_file, "r") as f:
        content = f.read()
    assert "CORRUPT_FIELD_NO_COLON" in content, f"{test_file} does not contain the extracted corrupted string."

def test_go_test_passes():
    processor_dir = "/home/user/processor"
    assert os.path.isdir(processor_dir), f"{processor_dir} is missing."

    result = subprocess.run(
        ["go", "test"],
        cwd=processor_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"`go test` failed in {processor_dir}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_processor_logic_fixed():
    # Create a temporary Go program to test ProcessTelemetry directly
    test_prog = """package main

import (
	"fmt"
	"processor"
)

func main() {
	res := processor.ProcessTelemetry("ID:8992|TEMP:12.4|STATUS:WARN|CORRUPT_FIELD_NO_COLON")
	if res["ID"] != "8992" || res["TEMP"] != "12.4" || res["STATUS"] != "WARN" {
		fmt.Println("FAILED")
	} else {
		fmt.Println("OK")
	}
}
"""
    prog_path = "/home/user/processor/verify_fix.go"
    with open(prog_path, "w") as f:
        f.write(test_prog)

    try:
        result = subprocess.run(
            ["go", "run", "verify_fix.go"],
            cwd="/home/user/processor",
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"ProcessTelemetry panicked or failed to compile when processing the corrupted string.\nStderr: {result.stderr}"
        assert result.stdout.strip() == "OK", "ProcessTelemetry did not return the expected parsed fields."
    finally:
        if os.path.exists(prog_path):
            os.remove(prog_path)