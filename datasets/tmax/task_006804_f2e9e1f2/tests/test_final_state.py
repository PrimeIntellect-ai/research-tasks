# test_final_state.py

import os
import pytest

def test_source_files_extracted():
    """Test that the source files were successfully extracted to the correct directory."""
    source_dir = "/home/user/source_files"
    assert os.path.isdir(source_dir), f"Directory {source_dir} does not exist."

    server_go = os.path.join(source_dir, "server.go")
    style_css = os.path.join(source_dir, "style.css")

    assert os.path.isfile(server_go), f"File {server_go} is missing. Archive extraction may have failed."
    assert os.path.isfile(style_css), f"File {style_css} is missing. Archive extraction may have failed."

def test_go_program_exists():
    """Test that the Go program was created at the correct location."""
    go_prog = "/home/user/process.go"
    assert os.path.isfile(go_prog), f"Go program {go_prog} is missing."

def test_final_report_content():
    """Test that the final report log contains the correctly formatted output."""
    report_path = "/home/user/final_report.log"
    assert os.path.isfile(report_path), f"Log file {report_path} is missing."

    expected_content = """[backend/server.go]
package main

import "fmt"

func main() {
	fmt.Println("Hello World")
}
[frontend/style.css]
body {
  background-color: #f0f0f0;
  margin: 0;
}
"""
    with open(report_path, "r") as f:
        actual_content = f.read()

    # Strip trailing whitespace to be resilient against minor newline differences at EOF
    assert actual_content.strip() == expected_content.strip(), "The contents of final_report.log do not match the expected format and data."