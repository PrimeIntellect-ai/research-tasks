# test_final_state.py

import os
import subprocess

def test_recovered_log():
    log_path = "/home/user/recovered.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. You must extract the valid transactions."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "SUCCESS: id=101, metric=2.5",
        "SUCCESS: id=102, metric=5.0",
        "SUCCESS: id=103, metric=8.1",
        "SUCCESS: id=104, metric=1.0"
    ]
    assert lines == expected, f"Content of {log_path} is incorrect. Expected exactly {len(expected)} specific SUCCESS lines, but got: {lines}"

def test_crash_csv():
    crash_path = "/home/user/crash.csv"
    assert os.path.isfile(crash_path), f"{crash_path} does not exist. You must identify the crashing line."

    with open(crash_path, "r") as f:
        content = f.read().strip()

    expected = "5,10,2.0"
    assert content == expected, f"Content of {crash_path} is incorrect. Expected '{expected}', got '{content}'."

def test_cargo_run_success():
    project_dir = "/home/user/fin-model"
    assert os.path.isdir(project_dir), f"{project_dir} does not exist."

    # Check if Cargo.toml has been fixed to not use edition 2025
    cargo_toml_path = os.path.join(project_dir, "Cargo.toml")
    assert os.path.isfile(cargo_toml_path), f"{cargo_toml_path} is missing."
    with open(cargo_toml_path, "r") as f:
        cargo_content = f.read()
    assert 'edition = "2025"' not in cargo_content, "Cargo.toml still contains the invalid edition '2025'."

    # Run cargo run to verify the build and the math bug fix
    result = subprocess.run(
        ["cargo", "run"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"cargo run failed with return code {result.returncode}.\n"
        f"Stdout: {result.stdout}\nStderr: {result.stderr}\n"
        "Ensure that the Cargo.toml is valid and the precision loss bug in main.rs is fixed."
    )

    assert "Result is not finite" not in result.stderr, "Panic 'Result is not finite' still occurs. The math bug is not fully fixed."