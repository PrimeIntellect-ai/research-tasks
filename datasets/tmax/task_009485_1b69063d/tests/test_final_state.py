# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/interp"

def test_build_tags():
    tape_linux_path = os.path.join(PROJECT_DIR, "tape_linux.go")
    tape_windows_path = os.path.join(PROJECT_DIR, "tape_windows.go")

    assert os.path.isfile(tape_linux_path), f"Missing {tape_linux_path}"
    with open(tape_linux_path, "r") as f:
        linux_content = f.read()
    assert "//go:build linux" in linux_content and "windows" not in linux_content.split('\n')[0], "tape_linux.go does not have the correct //go:build linux tag."

    assert os.path.isfile(tape_windows_path), f"Missing {tape_windows_path}"
    with open(tape_windows_path, "r") as f:
        windows_content = f.read()
    assert "//go:build windows" in windows_content and "!" not in windows_content.split('\n')[0], "tape_windows.go does not have the correct //go:build windows tag."

def test_make_builds():
    # Test make build-linux
    res_linux = subprocess.run(["make", "build-linux"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert res_linux.returncode == 0, f"make build-linux failed:\n{res_linux.stderr}"
    assert os.path.isfile(os.path.join(PROJECT_DIR, "interp-linux")), "interp-linux binary was not created."

    # Test make build-windows
    res_windows = subprocess.run(["make", "build-windows"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert res_windows.returncode == 0, f"make build-windows failed:\n{res_windows.stderr}"
    assert os.path.isfile(os.path.join(PROJECT_DIR, "interp-windows.exe")), "interp-windows.exe binary was not created."

def test_output_dat():
    output_dat_path = os.path.join(PROJECT_DIR, "output.dat")
    assert os.path.isfile(output_dat_path), f"output.dat is missing at {output_dat_path}"

    with open(output_dat_path, "r") as f:
        content = f.read()

    assert content == "Hello World!\n", f"output.dat does not contain the expected output. Got: {repr(content)}"

def test_bench_txt():
    bench_txt_path = os.path.join(PROJECT_DIR, "bench.txt")
    assert os.path.isfile(bench_txt_path), f"bench.txt is missing at {bench_txt_path}"

    with open(bench_txt_path, "r") as f:
        content = f.read()

    assert "BenchmarkTape" in content, "bench.txt does not contain 'BenchmarkTape'"
    assert "ns/op" in content, "bench.txt does not contain 'ns/op'"