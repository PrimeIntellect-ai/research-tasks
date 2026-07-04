# test_final_state.py

import os
import subprocess
import tempfile
import glob
import pytest

SANITIZE_SCRIPT = "/home/user/sanitize_loc.sh"
PROCESS_SCRIPT = "/home/user/process_all.sh"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"
COMPILER = "/app/i18n_compiler"

def run_script(script, *args):
    cmd = ["bash", script] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def test_sanitize_clean_corpus():
    """Test that sanitize_loc.sh preserves all rows in clean corpus files."""
    assert os.path.isfile(SANITIZE_SCRIPT), f"{SANITIZE_SCRIPT} does not exist."

    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.csv"))
    assert clean_files, "No clean corpus files found."

    failed_files = []

    for input_csv in clean_files:
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_out:
            output_csv = tmp_out.name

        try:
            res = run_script(SANITIZE_SCRIPT, input_csv, output_csv)
            assert res.returncode == 0, f"Script failed on {input_csv} with error: {res.stderr}"

            with open(input_csv, "r", encoding="utf-8") as f:
                input_lines = [line.strip() for line in f if line.strip()]

            with open(output_csv, "r", encoding="utf-8") as f:
                output_content = f.read()
                output_lines = [line.strip() for line in output_content.split("\n") if line.strip()]

            # Check for standard Unix (LF) line endings
            assert "\r\n" not in output_content, f"Output of {input_csv} contains CRLF line endings."

            if input_lines != output_lines:
                failed_files.append(os.path.basename(input_csv))
        finally:
            if os.path.exists(output_csv):
                os.remove(output_csv)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}")

def test_sanitize_evil_corpus():
    """Test that sanitize_loc.sh drops all evil rows in evil corpus files."""
    assert os.path.isfile(SANITIZE_SCRIPT), f"{SANITIZE_SCRIPT} does not exist."

    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.csv"))
    assert evil_files, "No evil corpus files found."

    failed_files = []

    for input_csv in evil_files:
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_out:
            output_csv = tmp_out.name

        try:
            res = run_script(SANITIZE_SCRIPT, input_csv, output_csv)
            assert res.returncode == 0, f"Script failed on {input_csv} with error: {res.stderr}"

            with open(output_csv, "r", encoding="utf-8") as f:
                output_content = f.read()
                output_lines = [line.strip() for line in output_content.split("\n") if line.strip()]

            # Check for standard Unix (LF) line endings
            assert "\r\n" not in output_content, f"Output of {input_csv} contains CRLF line endings."

            # The evil files provided in the setup contain ONLY evil rows (plus header).
            # Therefore, output should ONLY contain the header.
            if len(output_lines) != 1 or output_lines[0] != "Key,Source,Target":
                failed_files.append(os.path.basename(input_csv))
        finally:
            if os.path.exists(output_csv):
                os.remove(output_csv)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}")

def test_process_all_orchestration():
    """Test that process_all.sh correctly orchestrates sanitization and compilation."""
    assert os.path.isfile(PROCESS_SCRIPT), f"{PROCESS_SCRIPT} does not exist."

    with tempfile.TemporaryDirectory() as input_dir, tempfile.TemporaryDirectory() as output_dir:
        # Create a mixed CSV
        mixed_csv = os.path.join(input_dir, "mixed.csv")
        with open(mixed_csv, "w", encoding="utf-8") as f:
            f.write("Key,Source,Target\r\n")
            f.write("ui.ok,Good {var},Bien {var}\r\n") # Clean
            f.write("ui.bad1,Bad {var},Mauvais {var2}\r\n") # Mismatch
            f.write("ui.bad2,Hello,Bonjour <script>alert(1)</script>\r\n") # XSS

        res = run_script(PROCESS_SCRIPT, input_dir, output_dir)
        assert res.returncode == 0, f"process_all.sh failed: {res.stderr}"

        expected_bin = os.path.join(output_dir, "mixed.bin")
        assert os.path.isfile(expected_bin), f"Expected compiled binary {expected_bin} was not created."

        # Verify the binary format manually or by checking its size/magic header
        with open(expected_bin, "rb") as f:
            content = f.read()

        assert content.startswith(b"\x7FINTL"), "Binary does not contain the correct magic header."

        # The binary should contain exactly 1 entry (the clean one)
        # 4 bytes magic + 4 bytes integer
        entry_count = int.from_bytes(content[5:9], byteorder="little")
        assert entry_count == 1, f"Expected 1 entry in binary, found {entry_count}."