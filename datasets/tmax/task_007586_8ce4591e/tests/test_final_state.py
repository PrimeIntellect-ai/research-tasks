# test_final_state.py

import os
import stat
import pytest

def test_output_txt_exists_and_content():
    path = "/home/user/sec_lib/output.txt"
    assert os.path.isfile(path), f"{path} is missing. The script may not have been run or output redirection failed."

    with open(path, "r") as f:
        content = f.read()

    expected_content = "javascript:%3Cscript%3Ealert(1)%3C/script%3E\n"
    assert content == expected_content, f"Content of {path} is incorrect. Expected '{expected_content}', but got '{content}'."

def test_run_tool_sh_exists_and_executable():
    path = "/home/user/sec_lib/run_tool.sh"
    assert os.path.isfile(path), f"{path} is missing. The bash script was not created."

    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"{path} is not executable. Run 'chmod +x {path}'."

def test_compiled_artifacts_exist():
    lib_path = "/home/user/sec_lib/liburlsec.so"
    tool_path = "/home/user/sec_lib/urltool"

    assert os.path.isfile(lib_path), f"{lib_path} is missing. The Makefile may not have built the shared library successfully."
    assert os.path.isfile(tool_path), f"{tool_path} is missing. The Makefile may not have built the executable successfully."