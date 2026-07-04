# test_final_state.py

import os
import pytest

def test_clean_metrics_content():
    clean_metrics_path = "/home/user/clean_metrics.csv"
    assert os.path.exists(clean_metrics_path), f"File {clean_metrics_path} does not exist."
    assert os.path.isfile(clean_metrics_path), f"{clean_metrics_path} is not a file."

    expected_content = """1672531200,es-ES,ui.button.save,15
1672531260,es-ES,ui.button.save,15
1672531320,es-ES,ui.button.save,20
1672531200,fr-FR,ui.button.cancel,0
1672531260,fr-FR,ui.button.cancel,5
1672531320,fr-FR,ui.button.cancel,5
1672531200,es-ES,ui.menu.file,10
1672531260,es-ES,ui.menu.file,10
1672531320,es-ES,ui.button.save,20
"""
    with open(clean_metrics_path, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"Content of {clean_metrics_path} does not match the expected final state."

def test_pipeline_log_content():
    log_path = "/home/user/pipeline.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    with open(log_path, "r") as f:
        content = f.read()

    assert "[INFO] Starting localization metrics pipeline" in content, "Log file missing INFO start message."
    assert "[SUCCESS] Clean metrics generated" in content, "Log file missing SUCCESS completion message."

def test_run_pipeline_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_c_program_exists():
    c_path = "/home/user/impute_loc.c"
    assert os.path.exists(c_path), f"C program {c_path} does not exist."