# test_final_state.py

import os
import stat

def test_project_graph_c_fixed():
    file_path = "/home/user/project_graph.c"
    assert os.path.exists(file_path), f"File {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        content = f.read()

    # The bug was `if (edges[i].product = edges[j].product)`
    # It should be fixed to `if (edges[i].product == edges[j].product)`
    assert "if (edges[i].product == edges[j].product)" in content, "The C file bug was not fixed. Expected `==` instead of `=`."
    assert "if (edges[i].product = edges[j].product)" not in content, "The C file still contains the bug (`=` instead of `==`)."

def test_project_graph_executable_exists():
    file_path = "/home/user/project_graph"
    assert os.path.exists(file_path), f"Executable {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    # Check if the file is executable
    st = os.stat(file_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"{file_path} is not executable."

def test_top_user_txt_content():
    file_path = "/home/user/top_user.txt"
    assert os.path.exists(file_path), f"Output file {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "1", f"Expected top_user.txt to contain '1', but found '{content}'."