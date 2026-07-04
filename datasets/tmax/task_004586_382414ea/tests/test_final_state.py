# test_final_state.py
import os
import subprocess
import pytest

def test_minimal_trigger_bin():
    path = "/home/user/minimal_trigger.bin"
    assert os.path.isfile(path), f"File {path} does not exist"
    with open(path, "rb") as f:
        data = f.read()
    assert data == b"\x02\x00\xff\xff", f"minimal_trigger.bin content is incorrect: {data.hex()}"

def test_report_txt():
    path = "/home/user/report.txt"
    assert os.path.isfile(path), f"File {path} does not exist"
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    assert len(lines) >= 2, "report.txt must contain at least two lines"
    assert lines[1] == "sec_analyzer::parser::parse_packet", f"Line 2 of report.txt is incorrect: {lines[1]}"
    assert lines[0].isdigit(), f"Line 1 of report.txt should be a line number, got: {lines[0]}"

def test_processor_uses_atomic():
    path = "/home/user/sec_analyzer/src/processor.rs"
    assert os.path.isfile(path), f"File {path} does not exist"
    with open(path, "r") as f:
        content = f.read()
    assert "AtomicUsize" in content, "processor.rs does not use AtomicUsize to fix the race condition"

def test_parser_fixed():
    path = "/home/user/sec_analyzer/src/parser.rs"
    assert os.path.isfile(path), f"File {path} does not exist"
    with open(path, "r") as f:
        content = f.read()
    # Ensure the malicious pointer dereference is removed or patched out
    assert "read_volatile" not in content or "0x1000000000" not in content, "parser.rs still contains the malicious out-of-bounds read"

def test_cargo_build_and_run():
    proj_dir = "/home/user/sec_analyzer"

    # Test cargo build
    build_res = subprocess.run(["cargo", "build"], cwd=proj_dir, capture_output=True, text=True)
    assert build_res.returncode == 0, f"cargo build failed:\n{build_res.stderr}"

    # Test cargo run
    run_res = subprocess.run(["cargo", "run", "--", "/home/user/trace.bin"], cwd=proj_dir, capture_output=True, text=True)
    assert run_res.returncode == 0, f"cargo run failed or crashed:\n{run_res.stderr}"