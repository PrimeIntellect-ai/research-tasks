# test_final_state.py

import os
import stat
import subprocess
import tempfile

def test_scripts_exist():
    assert os.path.isfile("/home/user/validate.sh"), "validate.sh is missing"
    assert os.path.isfile("/home/user/bootstrap.py"), "bootstrap.py is missing"
    assert os.path.isfile("/home/user/pipeline.sh"), "pipeline.sh is missing"

def test_scripts_executable():
    assert os.access("/home/user/validate.sh", os.X_OK), "validate.sh is not executable"
    assert os.access("/home/user/pipeline.sh", os.X_OK), "pipeline.sh is not executable"

def test_pipeline_execution_and_outputs():
    # Run the pipeline
    result = subprocess.run(["/home/user/pipeline.sh"], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"pipeline.sh failed with exit code {result.returncode}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    # Check ci.txt
    assert os.path.isfile("/home/user/ci.txt"), "ci.txt was not generated"
    with open("/home/user/ci.txt", "r") as f:
        ci_content = f.read().strip()
    assert ci_content == "94.70,117.70", f"ci.txt content is incorrect. Expected '94.70,117.70', got '{ci_content}'"

    # Check plot.png
    assert os.path.isfile("/home/user/plot.png"), "plot.png was not generated"
    with open("/home/user/plot.png", "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", "plot.png is not a valid PNG file"

def test_validate_sh_bad_csv():
    # Create a bad CSV
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        tmp.write("transaction_id,amount,category\n")
        tmp.write("1,100\n") # Missing category
        tmp_path = tmp.name

    try:
        result = subprocess.run(["/home/user/validate.sh", tmp_path], capture_output=True)
        assert result.returncode == 1, "validate.sh should exit with status 1 for an invalid CSV"
    finally:
        os.remove(tmp_path)

def test_validate_sh_bad_header():
    # Create a bad CSV
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        tmp.write("id,amount,category\n")
        tmp.write("1,100,A\n")
        tmp_path = tmp.name

    try:
        result = subprocess.run(["/home/user/validate.sh", tmp_path], capture_output=True)
        assert result.returncode == 1, "validate.sh should exit with status 1 for an invalid header"
    finally:
        os.remove(tmp_path)