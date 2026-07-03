# test_final_state.py
import os
import subprocess
import tempfile

WORKSPACE = "/home/user/workspace"

def test_files_exist():
    expected_files = [
        "manifest_parser.c",
        "Makefile",
        "benchmark.sh"
    ]
    for f in expected_files:
        path = os.path.join(WORKSPACE, f)
        assert os.path.isfile(path), f"Expected file {path} is missing."

def test_makefile():
    # Test make clean
    subprocess.run(["make", "clean"], cwd=WORKSPACE, check=False)
    assert not os.path.exists(os.path.join(WORKSPACE, "parser_server")), "make clean did not remove parser_server"
    assert not os.path.exists(os.path.join(WORKSPACE, "parser_edge")), "make clean did not remove parser_edge"

    # Test make server
    res = subprocess.run(["make", "server"], cwd=WORKSPACE, capture_output=True)
    assert res.returncode == 0, f"make server failed: {res.stderr.decode()}"
    assert os.path.isfile(os.path.join(WORKSPACE, "parser_server")), "parser_server binary not created"

    # Test make edge
    res = subprocess.run(["make", "edge"], cwd=WORKSPACE, capture_output=True)
    assert res.returncode == 0, f"make edge failed: {res.stderr.decode()}"
    assert os.path.isfile(os.path.join(WORKSPACE, "parser_edge")), "parser_edge binary not created"

def test_parser_server():
    server_bin = os.path.join(WORKSPACE, "parser_server")

    valid_content = "[APP] my-app-1 v1.0.0\n[LIB] core-lib v0.9.15\n[SYS] kernel-module v5.15.0\n"
    invalid_type = "[UNK] my-app-1 v1.0.0\n"
    invalid_name = "[APP] my_app_1 v1.0.0\n"
    invalid_version = "[APP] my-app-1 v1.0\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        valid_file = os.path.join(tmpdir, "valid.txt")
        with open(valid_file, "w") as f:
            f.write(valid_content)

        res = subprocess.run([server_bin, valid_file], capture_output=True, text=True)
        assert res.returncode == 0, "SERVER mode failed on valid input"
        assert res.stdout.strip() == "SUCCESS: Parsed 3 packages.", f"Unexpected SERVER mode output: {res.stdout}"

        for name, content in [("inv_type.txt", invalid_type), ("inv_name.txt", invalid_name), ("inv_ver.txt", invalid_version)]:
            inv_file = os.path.join(tmpdir, name)
            with open(inv_file, "w") as f:
                f.write(content)
            res = subprocess.run([server_bin, inv_file], capture_output=True, text=True)
            assert res.returncode == 1, f"SERVER mode should fail on {name}"

def test_parser_edge():
    edge_bin = os.path.join(WORKSPACE, "parser_edge")

    valid_content = "[APP] my-app-1 v1.0.0\n[LIB] core-lib v0.9.15\n[SYS] kernel-module v5.15.0\n"
    invalid_type = "[UNK] my-app-1 v1.0.0\n"
    invalid_name = "[APP] my_app_1 v1.0.0\n"
    invalid_version = "[APP] my-app-1 v1.0\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        valid_file = os.path.join(tmpdir, "valid.txt")
        with open(valid_file, "w") as f:
            f.write(valid_content)

        res = subprocess.run([edge_bin, valid_file], capture_output=True, text=True)
        assert res.returncode == 0, "EDGE mode failed on valid input"
        assert res.stdout == "", f"EDGE mode should not produce output, got: {res.stdout}"

        for name, content in [("inv_type.txt", invalid_type), ("inv_name.txt", invalid_name), ("inv_ver.txt", invalid_version)]:
            inv_file = os.path.join(tmpdir, name)
            with open(inv_file, "w") as f:
                f.write(content)
            res = subprocess.run([edge_bin, inv_file], capture_output=True, text=True)
            assert res.returncode == 1, f"EDGE mode should fail on {name}"

def test_benchmark_script():
    script_path = os.path.join(WORKSPACE, "benchmark.sh")
    subprocess.run(["chmod", "+x", script_path], check=True)

    # Run benchmark script
    res = subprocess.run([script_path], cwd=WORKSPACE, capture_output=True)
    assert res.returncode == 0, f"benchmark.sh failed to execute: {res.stderr.decode()}"

    manifest_path = os.path.join(WORKSPACE, "large_manifest.txt")
    assert os.path.isfile(manifest_path), "large_manifest.txt was not created"

    with open(manifest_path, "r") as f:
        lines = f.readlines()
    assert len(lines) == 50000, f"large_manifest.txt expected 50000 lines, got {len(lines)}"

    results_path = os.path.join(WORKSPACE, "benchmark_results.txt")
    assert os.path.isfile(results_path), "benchmark_results.txt was not created"

    with open(results_path, "r") as f:
        content = f.read()
    assert "DONE" in content, "benchmark_results.txt does not contain 'DONE'"