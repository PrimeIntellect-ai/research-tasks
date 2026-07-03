# test_final_state.py
import os
import stat
import subprocess
import pytest

def test_generate_payload_sh_exists_and_executable():
    path = "/home/user/generate_payload.sh"
    assert os.path.exists(path), f"{path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

def test_generate_payload_sh_output():
    path = "/home/user/generate_payload.sh"
    assert os.path.exists(path), f"{path} does not exist."

    expected_output = "01:416c7068614e6f6465-QWxwaGFOb2Rl_02|02:426574614e6f6465-QmV0YU5vZGU=_03|03:47616d6d615465726d696e616c-R2FtbWFUZXJtaW5hbA==_00"

    result = subprocess.run([path], capture_output=True, text=True)
    assert result.stdout.strip() == expected_output, f"Output of {path} does not match the expected payload."

def test_ci_pipeline_sh_exists_and_executable():
    path = "/home/user/ci_pipeline.sh"
    assert os.path.exists(path), f"{path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

def test_ci_artifact_log_content():
    path = "/home/user/ci_artifact.log"
    assert os.path.exists(path), f"{path} does not exist. Did you run ci_pipeline.sh?"
    assert os.path.isfile(path), f"{path} is not a file."

    expected_content = (
        "PIPELINE_START\n"
        "01:416c7068614e6f6465-QWxwaGFOb2Rl_02|02:426574614e6f6465-QmV0YU5vZGU=_03|03:47616d6d615465726d696e616c-R2FtbWFUZXJtaW5hbA==_00\n"
        "GammaTerminal\n"
        "PIPELINE_SUCCESS"
    )

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {path} does not match the expected format."