# test_final_state.py
import os
import tarfile
import pytest

def test_tarball_exists_and_contents(tmp_path):
    tarball_path = "/home/user/quick_prints.tar.gz"
    assert os.path.isfile(tarball_path), f"Tarball {tarball_path} does not exist."

    expected_files = {
        "quick_prints/bench.gcode",
        "quick_prints/token.gcode",
        "quick_prints/almost.gcode"
    }

    unexpected_files = {
        "quick_prints/big_statue.gcode",
        "quick_prints/edge_case.gcode",
        "quick_prints/invalid.txt"
    }

    with tarfile.open(tarball_path, "r:gz") as tar:
        members = tar.getnames()

        # Check that expected files are in the tarball
        for f in expected_files:
            assert f in members, f"Expected file {f} missing from tarball {tarball_path}."

        # Check that unexpected files are NOT in the tarball
        for f in unexpected_files:
            assert f not in members, f"Unexpected file {f} found in tarball {tarball_path}."

def test_hard_links_created():
    quick_prints_dir = "/home/user/quick_prints"
    gcode_dir = "/home/user/gcode_files"

    assert os.path.isdir(quick_prints_dir), f"Directory {quick_prints_dir} does not exist."

    expected_files = ["bench.gcode", "token.gcode", "almost.gcode"]

    for filename in expected_files:
        src_path = os.path.join(gcode_dir, filename)
        dest_path = os.path.join(quick_prints_dir, filename)

        assert os.path.isfile(dest_path), f"Expected file {dest_path} does not exist."

        src_stat = os.stat(src_path)
        dest_stat = os.stat(dest_path)

        assert src_stat.st_ino == dest_stat.st_ino, f"{dest_path} is not a hard link to {src_path}."
        assert src_stat.st_dev == dest_stat.st_dev, f"{dest_path} and {src_path} are on different devices."

def test_no_extra_files_in_quick_prints():
    quick_prints_dir = "/home/user/quick_prints"
    if not os.path.isdir(quick_prints_dir):
        pytest.fail(f"Directory {quick_prints_dir} does not exist.")

    actual_files = set(os.listdir(quick_prints_dir))
    expected_files = {"bench.gcode", "token.gcode", "almost.gcode"}

    extra_files = actual_files - expected_files
    assert not extra_files, f"Unexpected files found in {quick_prints_dir}: {extra_files}"