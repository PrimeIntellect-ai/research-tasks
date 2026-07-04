# test_final_state.py
import os
import subprocess

def test_cargo_test_passes():
    project_dir = "/home/user/stats_project"
    assert os.path.isdir(project_dir), f"Project directory {project_dir} is missing."

    result = subprocess.run(
        ["cargo", "test"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed. stdout:\n{result.stdout}\nstderr:\n{result.stderr}"

def test_fix_txt_content():
    fix_txt_path = "/home/user/fix.txt"
    assert os.path.isfile(fix_txt_path), f"{fix_txt_path} is missing."

    with open(fix_txt_path, "r") as f:
        content = f.read().strip()

    expected = "let var = mean_sq - mean.powi(2);"
    assert content == expected, f"Expected fix.txt to contain exactly '{expected}', but got '{content}'"