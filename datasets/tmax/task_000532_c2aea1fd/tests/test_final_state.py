# test_final_state.py
import os
import subprocess
import pytest
import stat

def test_ci_run_script():
    script_path = "/home/user/ci-run.sh"
    assert os.path.isfile(script_path), f"Expected script {script_path} to exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Expected {script_path} to be executable."

    # Run the script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"ci-run.sh failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_symlink_and_directory():
    backend_dir = "/home/user/backend"
    symlink_path = "/home/user/active-upstream.sock"

    assert os.path.isdir(backend_dir), f"Expected directory {backend_dir} to exist."
    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symbolic link."
    assert os.readlink(symlink_path) == "/home/user/backend/app.sock", f"Symlink {symlink_path} does not point to /home/user/backend/app.sock."

def test_makefile_fixed():
    makefile_path = "/app/safe-router-1.1.0/Makefile"
    assert os.path.isfile(makefile_path), "Makefile is missing."
    with open(makefile_path, "r") as f:
        lines = f.readlines()

    # Check if tabs are used for targets
    has_tabs = any(line.startswith("\t") for line in lines)
    assert has_tabs, "Makefile does not seem to be fixed (no tab characters found for recipes)."

def test_main_go_fixed():
    main_go_path = "/app/safe-router-1.1.0/main.go"
    assert os.path.isfile(main_go_path), "main.go is missing."
    with open(main_go_path, "r") as f:
        content = f.read()

    assert "UPSTREAM_SOCK" in content, "main.go does not seem to read the UPSTREAM_SOCK environment variable."
    assert "/var/run/broken.sock" not in content, "main.go still contains the hardcoded broken socket path."

def test_adversarial_corpus():
    # Write a small Go program to test IsMalicious per file
    test_go_code = """package main

import (
	"bufio"
	"fmt"
	"net/http"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		os.Exit(1)
	}
	file, err := os.Open(os.Args[1])
	if err != nil {
		fmt.Println("ERROR")
		os.Exit(1)
	}
	defer file.Close()

	req, err := http.ReadRequest(bufio.NewReader(file))
	if err != nil {
		fmt.Println("ERROR")
		os.Exit(1)
	}

	if IsMalicious(req) {
		fmt.Println("REJECT")
	} else {
		fmt.Println("ALLOW")
	}
}
"""
    test_go_path = "/app/safe-router-1.1.0/pytest_runner.go"
    with open(test_go_path, "w") as f:
        f.write(test_go_code)

    # Compile the test runner
    build_cmd = ["go", "build", "-o", "pytest_runner", "filter.go", "pytest_runner.go"]
    build_res = subprocess.run(build_cmd, cwd="/app/safe-router-1.1.0", capture_output=True, text=True)
    assert build_res.returncode == 0, f"Failed to compile test runner:\n{build_res.stderr}"

    runner_path = "/app/safe-router-1.1.0/pytest_runner"

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".http")]
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".http")]

    evil_bypassed = []
    for f in evil_files:
        fpath = os.path.join(evil_dir, f)
        res = subprocess.run([runner_path, fpath], capture_output=True, text=True)
        if "REJECT" not in res.stdout:
            evil_bypassed.append(f)

    clean_modified = []
    for f in clean_files:
        fpath = os.path.join(clean_dir, f)
        res = subprocess.run([runner_path, fpath], capture_output=True, text=True)
        if "ALLOW" not in res.stdout:
            clean_modified.append(f)

    # Cleanup
    os.remove(test_go_path)
    if os.path.exists(runner_path):
        os.remove(runner_path)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)