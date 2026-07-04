# test_final_state.py

import os
import subprocess
import pytest

def test_answer_txt_content():
    path = "/home/user/answer.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The task requires writing the final integer output here."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "10000000", f"Expected answer '10000000' in {path}, but found '{content}'."

def test_calc_executable_fixed():
    executable_path = "/home/user/engine/calc"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

    # Run the executable with the crashing arguments
    try:
        result = subprocess.run(
            [executable_path, "100000.0", "0.001"],
            capture_output=True,
            text=True,
            timeout=2,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"The executable crashed or returned an error when run with '100000.0 0.001'. Return code: {e.returncode}. Output: {e.output}")
    except subprocess.TimeoutExpired:
        pytest.fail("The executable timed out when run with '100000.0 0.001'.")

    output = result.stdout.strip()
    assert output == "10000000", f"Expected the fixed executable to output '10000000', but got '{output}'."

def test_calc_c_modified():
    source_path = "/home/user/engine/calc.c"
    assert os.path.isfile(source_path), f"Source file {source_path} does not exist."

    with open(source_path, "r") as f:
        content = f.read()

    # The fix should involve changing floats to doubles or fixing the logic to avoid precision loss.
    # We can just rely on the executable test, but we can also ensure the source file is present and compiles.
    # The compilation check is implicitly covered by the executable test if the user recompiled it.
    # Just checking it exists and is readable is enough.
    assert len(content) > 0, f"Source file {source_path} is empty."