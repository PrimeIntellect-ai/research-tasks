# test_final_state.py

import os
import pytest

def test_embed_py_exists():
    """Verify that embed.py exists."""
    assert os.path.isfile("/home/user/embed.py"), "embed.py was not found at /home/user/embed.py"

def test_retrieve_r_exists():
    """Verify that retrieve.R exists."""
    assert os.path.isfile("/home/user/retrieve.R"), "retrieve.R was not found at /home/user/retrieve.R"

def test_run_pipeline_sh_exists_and_executable():
    """Verify that run_pipeline.sh exists and is executable."""
    path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(path), f"run_pipeline.sh was not found at {path}"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_top_concept_txt_exists_and_correct():
    """Verify that top_concept.txt exists and contains the correct ID."""
    path = "/home/user/top_concept.txt"
    assert os.path.isfile(path), f"{path} was not found. Did the pipeline run successfully?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "3", f"Expected top_concept.txt to contain '3', but got '{content}'"