# test_final_state.py

import os
from pathlib import Path

def test_report_exists():
    report_path = Path("/home/user/report.txt")
    assert report_path.is_file(), f"Report file {report_path} does not exist. Did you create it?"

def test_report_content():
    report_path = Path("/home/user/report.txt")
    assert report_path.is_file(), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "Packet: 4\nPayload: fffebaadf00d0000"

    assert content == expected_content, (
        f"The content of {report_path} is incorrect.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )

def test_build_rs_fixed():
    build_rs_path = Path("/home/user/diagnostic_workspace/pcap_ingest/build.rs")
    assert build_rs_path.is_file(), f"build.rs {build_rs_path} is missing."

    with open(build_rs_path, "r") as f:
        lines = f.readlines()

    # Check if the search path was uncommented or added
    search_path_added = any(
        "cargo:rustc-link-search=native=" in line and not line.strip().startswith("//")
        for line in lines
    )

    assert search_path_added, "build.rs does not contain an active 'cargo:rustc-link-search' directive. The build environment was not fixed."