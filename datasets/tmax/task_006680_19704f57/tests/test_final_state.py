# test_final_state.py

import os
import subprocess
import sqlite3
from pathlib import Path

def test_makefile_fixed():
    makefile_path = "/home/user/case_1029/src/Makefile"
    assert os.path.isfile(makefile_path), f"File {makefile_path} is missing"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-lz" in content, "Makefile does not link the zlib library (-lz)."

def test_parsed_logs():
    logs_path = "/home/user/case_1029/parsed_logs.txt"
    assert os.path.isfile(logs_path), f"File {logs_path} is missing"
    with open(logs_path, "r") as f:
        content = f.read()

    assert "System Bootup" in content, "parsed_logs.txt is missing the first record."
    assert "Service Started" in content, "parsed_logs.txt is missing the second record."

def test_db_dump():
    dump_path = "/home/user/case_1029/db_dump.txt"
    assert os.path.isfile(dump_path), f"File {dump_path} is missing"
    with open(dump_path, "r") as f:
        content = f.read()

    assert "Init" in content, "db_dump.txt is missing row 1."
    assert "Disk IO error" in content, "db_dump.txt is missing row 2 (from WAL)."
    assert "Emergency shutdown triggered" in content, "db_dump.txt is missing row 3 (from WAL)."

def test_mre_generator():
    base_dir = Path("/home/user/case_1029")
    mre_bin = base_dir / "mre.bin"

    if mre_bin.exists():
        mre_bin.unlink()

    # Find the MRE generator script
    scripts = list(base_dir.glob("make_mre.*"))
    assert scripts, "MRE generator script (e.g., make_mre.py or make_mre.sh) is missing."

    script_path = scripts[0]

    # Run the script
    if script_path.suffix == ".py":
        subprocess.run(["python3", str(script_path)], cwd=str(base_dir), check=True)
    elif script_path.suffix == ".sh":
        subprocess.run(["bash", str(script_path)], cwd=str(base_dir), check=True)
    else:
        # Try to execute directly
        subprocess.run([str(script_path)], cwd=str(base_dir), check=True)

    assert mre_bin.exists(), "MRE generator did not create mre.bin."

    with open(mre_bin, "rb") as f:
        data = f.read()

    assert len(data) >= 6, "mre.bin is too small to contain a valid header and length."
    assert data[:4] == b"DATA", "mre.bin does not start with the correct 'DATA' magic bytes."

    expected_len = int.from_bytes(data[4:6], "little")
    actual_payload_len = len(data) - 6

    assert actual_payload_len < expected_len, (
        f"mre.bin is not truncated. Expected {expected_len} payload bytes, "
        f"but found {actual_payload_len}."
    )